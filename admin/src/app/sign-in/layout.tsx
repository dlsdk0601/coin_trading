import React, { PropsWithChildren, Suspense } from "react";

const Layout = (props: PropsWithChildren) => {
  return (
    <div className="flex h-screen flex-wrap items-center justify-center">
      <div className="border-stroke shadow-default dark:border-strokedark dark:bg-boxdark w-3/4 rounded-sm border bg-white xl:w-1/3">
        <div className="w-full p-3 sm:p-12.5 xl:p-17.5">
          <h2 className="sm:text-title-xl2 mb-9 text-2xl font-bold text-black dark:text-white">
            Sign In to Portfolio Admin
          </h2>

          <Suspense>{props.children}</Suspense>
        </div>
      </div>
    </div>
  );
};

export default Layout;
