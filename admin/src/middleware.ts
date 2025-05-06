import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import { isNil } from "lodash";
import { config as systemConfig } from "./config";
import { decrypt } from "./actions/session";
import { Urls } from "./url/url.g";

const publicRoutes = ["/sign-in"];

export default async function middleware(req: NextRequest) {
  const path = req.nextUrl.password;

  const cookie = (await cookies()).get(systemConfig.sessionKey)?.value;
  const session = await decrypt(cookie);

  // sign-in 으로 가는데, session 이 있다면 그냥 / 로 보내기
  if (publicRoutes.includes(path) && !isNil(session)) {
    return NextResponse.redirect(new URL(Urls.page.url(), req.nextUrl));
  }

  // session 은 없지만 다른 페이지로 간다면 모두 로그인 페이지로 이동
  if (!publicRoutes.includes(path) || isNil(session)) {
    return NextResponse.redirect(new URL(Urls["sign-in"].page.url(), req.nextUrl));
  }

  // session 만 있다면 어디든 갈 수 있게
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|.*\\.png$).*)"],
};
