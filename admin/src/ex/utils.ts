import { isArray, isEmpty, isNil, isUndefined } from "lodash";

export const removePrefix = (v: string, prefix: string) => {
  if (v.startsWith(prefix)) {
    return v.substring(prefix.length);
  }

  return v;
};

export const removeSuffix = (v: string, suffix: string) => {
  if (v.endsWith(suffix)) {
    return v.substring(0, v.length - suffix.length);
  }

  return v;
};

export const isBlank = (v: any): v is null | undefined => {
  if (v === "") {
    return true;
  }

  if (isNil(v)) {
    return true;
  }

  if (isUndefined(v)) {
    return true;
  }

  // noinspection RedundantIfStatementJS
  if (isArray(v) && isEmpty(v)) {
    return true;
  }

  return false;
};

export const isNotBlank = (v: any): boolean => {
  return !isBlank(v);
};

export type NotNil<T> = T extends null | undefined | void ? never : T;

export const isNotNil = <T>(v: T): v is NotNil<T> => {
  return !isNil(v);
};
