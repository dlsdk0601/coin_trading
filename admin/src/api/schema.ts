export type ResStatus =
  | "OK"
  | "INVALID_ACCESS_TOKEN"
  | "NO_PERMISSION"
  | "NOT_FOUND"
  | "LOGIN_REQUIRED";

export interface PydanticValidationError {
  loc: string[];
  msg: string;
}

export interface Res<T> {
  data: T | null;
  errors: string[];
  validationErrors: PydanticValidationError[];
  status: ResStatus;
}

export interface ResError {
  error: string;
}

export interface SignInReq {
  id: string;
  password: string;
}

export interface SignInRes {
  token: string;
}

export interface SignOutReq {}

export interface SignOutRes {}

export interface SignReq {}

export interface SignRes {
  pk: number;
  id: string;
}
