import { isNil, map } from "lodash";
import { cookies } from "next/headers";
import {
  ConfigListReq,
  ConfigListRes,
  PydanticValidationError,
  Res,
  ResError,
  ResStatus,
  SignInReq,
  SignInRes,
  SignOutReq,
  SignOutRes,
  SignReq,
  SignRes,
} from "./schema";
import { config } from "../config";
import { isNotNil } from "../ex/utils";
import { decrypt } from "../actions/session";

export interface ApiHandler {
  catch(e: any): void;

  handleValidationErrors(errors: PydanticValidationError[]): string;

  handlerErrors(errors: string[]): string;

  handleStatus(status: ResStatus): string;

  beforeRequest(headers: Record<string, string>): Promise<void>;
}

class Handler implements ApiHandler {
  catch(e: any) {
    console.error(e);
    throw new Error(e);
  }

  handleValidationErrors(errors: PydanticValidationError[]) {
    console.error(...errors);

    const messages = map(errors, (err) => `${err.loc} : ${err.msg}`).join("\n");
    if (messages) {
      return messages;
    }
    return JSON.stringify(errors, null, 2);
  }

  handlerErrors(errors: string[]) {
    console.error(...errors);
    return errors.join("\n");
  }

  handleStatus(status: ResStatus) {
    switch (status) {
      case "OK":
        return "";
      case "NO_PERMISSION":
        return "해당 기능의 권한이 없습니다.";
      case "INVALID_ACCESS_TOKEN":
        return "로그인을 재시도 해주세요.";
      case "LOGIN_REQUIRED":
        return "로그인 페이지로 이동합니다.";
      case "NOT_FOUND":
      default: {
        return "존재하지 않는 페이지 또는 데이터입니다.";
      }
    }
  }

  async beforeRequest(headers: Record<string, string>) {
    let token: string | null = null;
    if (typeof window !== "undefined" && isNotNil(sessionStorage)) {
      token = sessionStorage.getItem(config.tokenKey);
    } else {
      const session = (await cookies()).get(config.sessionKey)?.value;
      const payload = await decrypt(session);
      if (isNotNil(payload)) {
        token = payload.token as string;
      }
    }

    if (isNotNil(token)) {
      headers["Authorization"] = token;
    }
  }
}

class ApiBase {
  private readonly baseUrl: string;
  private readonly handler: ApiHandler;

  constructor(baseUrl: string, handler: ApiHandler) {
    this.baseUrl = baseUrl;
    this.handler = handler;
  }

  async f<U>(url: string, req: any): Promise<U | ResError> {
    try {
      const headers: Record<string, string> = {};
      await this.handler.beforeRequest(headers);
      let body = req;
      if (!(body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
        body = JSON.stringify(req);
      }
      const response = await fetch(this.baseUrl + url, {
        method: "POST",
        mode: "cors",
        credentials: "include",
        headers,
        body,
        cache: "no-cache",
      });

      const res: Res<U> = await response.json();
      return this.handleResponse(res);
    } catch (e) {
      this.handler.catch(e);
      return { error: "알 수 없는 에러가 발생했습니다. [100]" };
    }
  }

  protected c<T, U>(url: string): (req: T) => Promise<U | ResError> {
    return async (req) => this.f(url, req);
  }

  private handleResponse<U>(res: Res<U>): U | ResError {
    if (res.status !== "OK") {
      const error = this.handler.handleStatus(res.status);
      return { error };
    }

    if (res.validationErrors.length) {
      const error = this.handler.handleValidationErrors(res.validationErrors);
      return { error };
    }

    if (res.errors.length) {
      const error = this.handler.handlerErrors(res.errors);
      return { error };
    }

    if (isNil(res.data)) {
      return { error: "알 수 없는 에러가 발생했습니다. [101]" };
    }

    return res.data;
  }
}

class Api extends ApiBase {
  signIn = this.c<SignInReq, SignInRes>("/sf/sign-in");
  sign = this.c<SignReq, SignRes>("/sf/sign");
  signOut = this.c<SignOutReq, SignOutRes>("/sf/sign-out");
  configList = this.c<ConfigListReq, ConfigListRes>("/sf/config-list");
}

const handler = new Handler();
export const api = new Api(config.apiBaseUrl, handler);
