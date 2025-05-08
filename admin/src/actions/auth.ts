"use server";

import { isNil } from "lodash";
import { FormRes, isError, SignInFormSchema } from "./definition";
import { api } from "../api/api";
import { createSession, deleteSession } from "./session";
import { SignInRes } from "../api/schema";

export async function signIn(state: FormRes<SignInRes>, formData: FormData) {
  const validatedFields = SignInFormSchema.safeParse({
    id: formData.get("id"),
    password: formData.get("password"),
  });

  if (!validatedFields.success) {
    const error = getErrorMessage(validatedFields.error.flatten().fieldErrors);
    return { error };
  }

  const { id, password } = validatedFields.data;

  const res = await api.signIn({ id, password });

  if (isError(res)) {
    return { error: res.error };
  }

  await createSession(res.token);

  return { data: { token: res.token } };
}

export async function signOut() {
  const res = await api.signOut({});

  if (isError(res)) {
    return { error: res.error };
  }

  await deleteSession();
}

function getErrorMessage(error: Record<string, string[] | undefined>): string {
  let message = "";

  for (const key of Object.keys(error)) {
    const v = error[key];
    if (isNil(v)) {
      continue;
    }

    message = v.at(0) ?? "";
    break;
  }

  return message;
}
