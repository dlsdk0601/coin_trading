import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import { isNil } from "lodash";
import { config as systemConfig } from "./config";
import { decrypt } from "./actions/session";
import { Urls } from "./url/url.g";

const publicRoutes = ["/sign-in"];

export default async function middleware(req: NextRequest) {
  const path = req.nextUrl.pathname;

  const cookie = (await cookies()).get(systemConfig.sessionKey)?.value;
  const session = await decrypt(cookie);

  // session 은 없으면 무조건 로그인 페이지로
  if (!publicRoutes.includes(path) && isNil(session)) {
    return NextResponse.redirect(new URL(Urls["sign-in"].page.url(), req.nextUrl));
  }

  // session 만 있다면 어디든 갈 수 있다
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|.*\\.(?:png|ico|jpg|jpeg|svg)$).*)"],
};
