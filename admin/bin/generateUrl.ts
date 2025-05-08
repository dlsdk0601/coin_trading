import { readdirSync, writeFileSync } from "node:fs";
import { readFileSync } from "fs";
import path from "node:path";
import { head } from "lodash";
import prettier from "prettier";
import { isBlank, removeSuffix } from "../src/ex/utils";

type Page = {
  kind: "page";
  readonly name: string;
  readonly query?: string;
};

type Dir = {
  kind: "dir";
  readonly name: string;
  readonly children: (Page | Dir)[];
};

const ignoreFiles = ["layout", "loading", "_"];

function parseSource(parentDir: string): (Page | Dir)[] {
  const entries = readdirSync(parentDir, { withFileTypes: true });
  const contents: (Page | Dir)[] = [];

  for (const entry of entries) {
    if (
      entry.isFile() &&
      entry.name.endsWith(".tsx") &&
      !ignoreFiles.includes(removeSuffix(entry.name, ".tsx"))
    ) {
      const tsx = readFileSync(path.join(parentDir, entry.name), { encoding: "utf-8" })
        .split("\n")
        .filter((line) => !line.trim().startsWith("//"))
        .join("\n");

      const queries: RegExpMatchArray[] = Array.from(tsx.matchAll(/interface Query\s*{[^}]*}/g));

      if (queries.length > 1) {
        throw new Error(`Query 가 두번 정의되었습니다. : file=${path.join(parentDir, entry.name)}`);
      }

      const query = Array.from(head(queries) ?? [])[0];

      contents.push({
        kind: "page",
        name: removeSuffix(entry.name, ".tsx"),
        query: query && query.replaceAll("interface Query", ""),
      });

      continue;
    }

    if (entry.isDirectory()) {
      const children = parseSource(path.join(parentDir, entry.name));
      if (isBlank(children)) {
        continue;
      }

      if (!entry.name.startsWith("(")) {
        contents.push({ kind: "dir", name: entry.name, children });
      }

      if (entry.name.startsWith("(")) {
        contents.push(...children);
      }
    }
  }

  return contents;
}

function generateSources(pages: (Page | Dir)[], parents: string[]): string[] {
  return pages.flatMap((page) => generateSource(page, parents));
}

function generateSource(page: Page | Dir, parents: string[]): string[] {
  const lines: string[] = [];
  const newParents = [...parents, page.name === "page" ? "" : page.name];

  switch (page.kind) {
    case "page": {
      const pathname = `/${newParents.join("/")}`;
      const key = `"${page.name}"`;
      const endpoint =
        pathname.endsWith("/") && pathname !== "/"
          ? pathname.substring(0, pathname.length - 1)
          : pathname;

      if (page.query) {
        lines.push(`${key}: new PageUrl<Partial<${page.query}>>("${endpoint}"),`);
      } else {
        lines.push(`${key}: new PageUrl("${endpoint}"),`);
      }
      break;
    }
    case "dir":
    default: {
      lines.push(`"${page.name}": {`);
      lines.push(...generateSources(page.children, newParents));
      lines.push("},");
      break;
    }
  }

  return lines;
}

const pagesDir = path.join(import.meta.dir, "..", "src/app");
const pages = parseSource(pagesDir);

const ts: string[] = [];
ts.push("/* tslint:disable */");
ts.push("/* eslint-disable */");
ts.push(`// 자동 생성 파일 수정하지 말것 ${new Date().toString()}`);
ts.push("import { PageUrl } from './url';\n");
// ts.push("import { cPk } from '../ex/query';");
ts.push("export const Urls = {");
ts.push(...generateSources(pages, []));
ts.push("};");

const target = path.join(import.meta.dir, "..", "src/url/url.g.ts");
prettier.format(ts.join("\n"), { filepath: target }).then((res) => writeFileSync(target, res)).then(() => console.log("done"));
