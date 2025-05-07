"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

export function Replace(props: { url: string }) {
  const router = useRouter();
  useEffect(() => {
    router.replace(props.url);
  }, [router, props.url]);
  return <></>;
}
