import "server-only";
import { cookies } from "next/headers";
import { JWTPayload, jwtVerify, SignJWT } from "jose";
import { isNil } from "lodash";
import { redirect } from "next/navigation";
import { now } from "../ex/dayjsEx";
import { config } from "../config";
import { Urls } from "../url/url.g";

export interface Payload extends JWTPayload {
  token: string;
  expiresAt: Date;
}

export async function encrypt(payload: Payload) {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("7d")
    .sign(config.encodedKey);
}

export async function decrypt(session: string = "") {
  try {
    const { payload } = await jwtVerify(session, config.encodedKey, {
      algorithms: ["HS256"],
    });
    return payload as Payload;
  } catch (err) {
    console.warn(`Failed to verify session, err=${err}`);
  }
}

export async function createSession(token: string) {
  const expiresAt = now()
    .add(7 * 24 * 60 * 60, "s")
    .toDate();
  const session = await encrypt({ token, expiresAt });
  await setCookies(session);
}

export async function updateSession() {
  const session = (await cookies()).get(config.sessionKey)?.value;
  const payload = await decrypt(session);

  if (isNil(session) || isNil(payload)) {
    return null;
  }

  await setCookies(session);
}

export async function setCookies(session: string) {
  const expiresAt = now()
    .add(7 * 24 * 60 * 60, "s")
    .toDate();
  const cookieStore = await cookies();
  cookieStore.set(config.sessionKey, session, {
    httpOnly: true,
    secure: true,
    expires: expiresAt,
    sameSite: "lax",
    path: "/",
  });
}

export async function deleteSession() {
  const cookieStore = await cookies();
  cookieStore.delete(config.sessionKey);
  redirect(Urls["sign-in"].page.url());
}
