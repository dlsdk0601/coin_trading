import { isNil } from "lodash";
import { isBlank } from "../ex/utils";

export class PageUrl<T extends Record<string, any>> {
  readonly pathname: string;

  constructor(pathname: string) {
    this.pathname = pathname;
  }

  url(query?: T) {
    let path = this.pathname;

    if (isNil(query)) {
      return path;
    }

    const q: Record<string, string> = {};

    Object.keys(query).forEach((item) => {
      if (isNil(query[item])) {
        return;
      }

      // query 값 중에 path 에 있다면 거기에 처리 한다.
      if (path.includes(item)) {
        path = this.pathname.replace(`[${item}]`, `${query[item]}`);
        return;
      }

      q[item] = `${query[item]}`;
    });

    const queryParams = new URLSearchParams(q);

    if (isBlank(queryParams.toString())) {
      return path;
    }

    return `${path}?${queryParams.toString()}`;
  }
}
