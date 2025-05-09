"use client";

import { Urls } from "../../url/url.g";
import Link from "next/link";

const Error = (props: {error: Error & { digest?: string }, reset: () => void}) => {

  return (
    <div className="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">
      <div className="rounded-sm border border-stroke bg-white px-5 py-10 shadow-default dark:border-strokedark dark:bg-boxdark sm:py-20">
        <div className="mx-auto max-w-[410px]">
          <img
            alt="illustration"
            className="h-[400px] w-[400px] text-transparent"
            src="/assets/images/illustration/illustration-01.svg"
          />
          <div className="mt-7.5 text-center">
            <h2 className="mb-3 text-2xl font-bold text-black dark:text-white">
              {props.error.message}
            </h2>
            <Link
              className="mt-7.5 inline-flex items-center gap-2 rounded-md bg-primary px-6 py-3 font-medium text-white hover:bg-opacity-90"
              href={Urls.page.url({})}
            >
              <i className="mdi mdi-keyboard-backspace text-2xl" />
              <span>Home 으로 돌아가기</span>
            </Link>
            <button
              className="cursor-pointer ms-7.5 inline-flex items-center gap-2 rounded-md bg-bodydark2 px-6 py-3 font-medium text-white hover:bg-opacity-90"
              onClick={() => props.reset}
            >
              <i className="mdi mdi-reload text-2xl" />
              <span>재시도 하기</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Error;