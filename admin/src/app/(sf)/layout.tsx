import { PropsWithChildren } from "react";
import { HeaderView } from "../../view/layout/HeaderView";
import LeftSidebarView from "../../view/layout/leftSidebarView";
import { getUser } from "../../actions/dal";

const Layout = async (props: PropsWithChildren) => {
  const user = await getUser();
  return (
    <div className="flex h-screen overflow-hidden">
      <LeftSidebarView user={user} />
      <div className="relative flex flex-1 flex-col overflow-x-hidden overflow-y-auto">
        <HeaderView />
        <main>
          <div className="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">{props.children}</div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
