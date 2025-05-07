"use client";

import Link from "next/link";
import { useActionState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { isNil } from "lodash";
import TextFieldView from "../../view/textFieldView";
import { EmailIcon, LockIcon } from "../../view/icons";
import { signIn } from "../../actions/auth";
import { config } from "../../config";
import { Urls } from "../../url/url.g";

const Page = () => {
  const router = useRouter();
  const [state, action, pending] = useActionState(signIn, undefined);

  useEffect(() => {
    if (pending) {
      return;
    }

    const token = state?.token;
    if (isNil(token)) {
      return;
    }

    sessionStorage.setItem(config.tokenKey, token);
    router.replace(Urls.page.url());
  }, [router, state, pending]);

  return (
    <form action={action}>
      <TextFieldView name="id" icon={<EmailIcon />} error={state?.errors?.id?.at(0)} />

      <TextFieldView
        type="password"
        name="password"
        icon={<LockIcon />}
        error={state?.errors?.password?.at(0)}
      />

      <div className="mb-5">
        <input
          type="submit"
          value="Sign In"
          disabled={pending}
          className="border-primary bg-primary hover:bg-opacity-90 w-full cursor-pointer rounded-lg border p-4 text-white transition"
        />
      </div>

      <div className="mt-6 text-center">
        <p>
          Don’t have any account?{" "}
          <Link href="mailto:inajung7008@gmail.com" className="text-primary">
            Send to email
          </Link>
        </p>
      </div>
    </form>
  );
};

export default Page;
