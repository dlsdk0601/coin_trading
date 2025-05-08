import { z } from "zod";
import { config } from "../config";
import { ResError } from "../api/schema";

export const SignInFormSchema = z.object({
  id: z.string().nonempty("id를 입력해주세요.").trim(),
  password: config.debug
    ? z.string().nonempty("비밀번호를 입력해주세요.").trim()
    : z
        .string()
        .min(8, { message: "비밀번호를 8글자 이상 입력해주세요." })
        .regex(/[a-zA-Z]/, { message: "비밀번호는 대문자를 포함해야합니다." })
        .regex(/[0-9]/, { message: "비밀번호는 숫자를 포함해야합니다." })
        .regex(/[^a-zA-Z0-9]/, { message: "비밀번호는 특수 문자를 포함해야합니다." })
        .trim(),
});

interface FormState<T> {
  data?: T;
  error?: string;
}

export type FormRes<T> = FormState<T> | undefined;

export function isError(res: any | ResError): res is ResError {
  return (res as ResError).error !== undefined;
}
