import { isNil, map } from "lodash";
import {
  AuthReq,
  AuthRes,
  PydanticValidationError,
  Res,
  ResStatus,
  SignInReq,
  SignInRes,
} from "./schema";
import { config } from "../config";

export interface ApiHandler {
  catch(e: any): void;

  handleValidationErrors(errors: PydanticValidationError[]): void;

  handlerErrors(errors: string[]): void;

  handleStatus(status: ResStatus): void;

  beforeRequest(headers: Record<string, string>): void;
}

class Handler implements ApiHandler {
  catch(e: any) {
    console.error(e);

    // TODO :: 여기서의 throw 가 컴포넌트에서 어떤 영향을 미칠지 확인
    throw e;
  }

  handleValidationErrors(errors: PydanticValidationError[]) {
    console.error(...errors);

    const messages = map(errors, (err) => `${err.loc} : ${err.msg}`).join("\n");
    if (messages) {
      throw new Error(messages);
    } else {
      throw new Error(JSON.stringify(errors, null, 2));
    }
  }

  handlerErrors(errors: string[]) {
    console.error(...errors);
    throw new Error(errors.join("\n"));
  }

  handleStatus(status: ResStatus) {
    switch (status) {
      case "OK":
        return;
      case "NO_PERMISSION":
        throw new Error("해당 기능의 권한이 없습니다.");
      case "INVALID_ACCESS_TOKEN":
        // TODO :: 비 로그인 유저도 고려 해야하는데, ERROR 정의를 어떻게 할지 후에 결정
        return;
      case "LOGIN_REQUIRED":
        throw new Error("로그인 페이지로 이동합니다.");
      case "NOT_FOUND":
      default: {
        throw new Error("존재하지 않는 페이지 또는 데이터입니다.");
      }
    }
  }

  beforeRequest(headers: Record<string, string>) {
    const token = sessionStorage.getItem(config.tokenKey);
    if (!isNil(token)) {
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

  async f<U>(url: string, req: any): Promise<U | null> {
    try {
      const headers: Record<string, string> = {};
      this.handler.beforeRequest(headers);
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
      return null;
    }
  }

  protected c<T, U>(url: string): (req: T) => Promise<U | null> {
    return async (req) => this.f(url, req);
  }

  private handleResponse<U>(res: Res<U>) {
    if (res.status !== "OK") {
      this.handler.handleStatus(res.status);
      return null;
    }

    if (res.validationErrors.length) {
      this.handler.handleValidationErrors(res.validationErrors);
      return null;
    }

    if (res.errors.length) {
      this.handler.handlerErrors(res.errors);
      return null;
    }

    return res.data;
  }
}

class Api extends ApiBase {
  signIn = this.c<SignInReq, SignInRes>("/sf/sign-in");
  auth = this.c<AuthReq, AuthRes>("/sf/auth");
}

const handler = new Handler();
export const api = new Api(config.apiBaseUrl, handler);
