import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import { isNil } from "lodash";
import { config as systemConfig } from "./config";
import { decrypt } from "./actions/session";
import { Urls } from "./url/url.g";
import { isNotNil } from "./ex/utils";

const publicRoutes = ["/sign-in"];

export default async function middleware(req: NextRequest) {
  const path = req.nextUrl.pathname;

  const cookie = (await cookies()).get(systemConfig.sessionKey)?.value;
  const session = await decrypt(cookie);

  const isRequireSignIn = isNil(session) && !publicRoutes.includes(path);
  // session 은 없으면 무조건 로그인 페이지로
  if (isRequireSignIn) {
    return NextResponse.redirect(new URL(Urls["sign-in"].page.url(), req.nextUrl));
  }

  // session 이 있는데 로그인 접속 하면 무조건 index 페이지로
  if (isNotNil(session) && publicRoutes.includes(path)) {
    return NextResponse.redirect(new URL(Urls.page.url(), req.nextUrl));
  }

  // session 만 있다면 어디든 갈 수 있다
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|.*\\.(?:png|ico|jpg|jpeg|svg)$).*)"],
};
