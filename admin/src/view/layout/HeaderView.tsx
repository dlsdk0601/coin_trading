import React from "react";
import { DarkModeSwitcher, LeftSidebarButtonView } from "./headerButtonView";
import DropDownUserView from "./DropDownUserView";

export const HeaderView = () => {
  return (
    <header className="sticky top-0 z-999 flex w-full bg-white drop-shadow-1 dark:bg-boxdark dark:drop-shadow-none">
      <div className="flex flex-grow items-center justify-between px-4 py-4 shadow-2 md:px-6 2xl:px-11">
        <LeftSidebarButtonView />
        <ul className="flex items-center gap-2 2xsm:gap-4">
          <DarkModeSwitcher />
        </ul>
        <DropDownUserView />
      </div>
    </header>
  );
};
