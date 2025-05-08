import "server-only";

import { cache } from "react";
import { cookies } from "next/headers";
import { isNil } from "lodash";
import { config } from "../config";
import { api } from "../api/api";
import { decrypt } from "./session";
import { redirect } from "next/navigation";
import { Urls } from "../url/url.g";
import { isError } from "./definition";

export const verifySession = cache(async () => {
  const cookie = (await cookies()).get(config.sessionKey)?.value;
  const session = await decrypt(cookie);

  if (isNil(session) || !session.token) {
    redirect(Urls["sign-in"].page.url());
  }

  return { isAuth: true, token: session.token };
});

export const getUser = cache(async () => {
  const session = await verifySession();

  if (isNil(session)) {
    return null;
  }

  try {
    const res = await api.sign({});

    if (isError(res)) {
      redirect(Urls["sign-in"].page.url());
    }

    return res;
  } catch (e) {
    console.error(e);
    return { error: "알 수 없는 에러가 발생했습니다. [102]" };
  }
});

export const a = () => {
  console.log("d");
};
