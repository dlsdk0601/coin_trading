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

  const token: string | undefined = session?.token;
  if (isNil(session) || isNil(token)) {
    return { isAuth: false, token: "" };
  }

  return { isAuth: true, token: session.token };
});

export const getUser = cache(async () => {
  const session = await verifySession();

  if (!session.isAuth) {
    redirect(Urls["sign-in"].page.url());
  }

  try {
    const res = await api.sign({});

    if (isError(res)) {
      redirect(Urls["sign-in"].page.url());
    }

    return res;
  } catch (e) {
    console.error(e);
    redirect(Urls["sign-in"].page.url());
  }
});
