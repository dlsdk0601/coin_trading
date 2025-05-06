import { z } from "zod";

export const SignInFormSchema = z.object({
  id: z.string().trim(),
  password: z
    .string()
    .min(8, { message: "8 글자 이상 입력해주세요." })
    .regex(/[a-zA-Z]/, { message: "대문자를 포함해야합니다." })
    .regex(/[0-9]/, { message: "숫자를 포함해야합니다." })
    .regex(/[^a-zA-Z0-9]/, { message: "특수 문자를 포함해야합니다." })
    .trim(),
});

export type FormState =
  | {
      errors?: {
        id?: string[];
        password?: string[];
      };
      message?: string;
    }
  | undefined;
