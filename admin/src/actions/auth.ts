import { isNil } from "lodash";
import { FormState, SignInFormSchema } from "./definition";
import { createSession } from "./session";
import { api } from "../api/api";

export async function signIn(state: FormState, formData: FormData) {
  const validatedFields = SignInFormSchema.safeParse({
    id: formData.get("id"),
    password: formData.get("password"),
  });

  if (!validatedFields.success) {
    return { errors: validatedFields.error.flatten().fieldErrors };
  }

  const { id, password } = validatedFields.data;

  const res = await api.signIn({ id, password });

  if (isNil(res)) {
    return { message: "API 통신 실패" };
  }

  await createSession(res.token);

  return { token: res.token };
}
