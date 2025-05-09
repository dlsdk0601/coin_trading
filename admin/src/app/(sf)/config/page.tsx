import { configList } from "../../../actions/config";
import { isError } from "../../../actions/definition";
import Link from "next/link";
import { TableView } from "../../../view/tableView";

const Page= async () => {
  const list = await configList();

  if(isError(list)){
    throw list.error;
  }
  
  if(list.items.length === 0){
    return <div className="rounded-sm px-5 pb-2.5 pt-6 dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
      <div className="mb-6 flex items-center justify-between">
        <h4 className="text-xl font-semibold text-black dark:text-white">
          Total: 0
        </h4>
          <Link
            href="/"
            className="block w-[100px] rounded border bg-success px-4 text-center font-medium text-white hover:opacity-80 dark:hover:opacity-80 sm:px-4 sm:py-3"
          >
            등록
          </Link>
      </div>
      <div className="h-[350px] max-w-full overflow-x-auto">
        <p className="my-5 text-center">조회된 데이터가 없습니다.</p>
      </div>
    </div>
  }

  return <section className="data-table-common rounded-sm border border-stroke bg-white py-4 shadow-default dark:border-strokedark dark:bg-boxdark">
    <div className="rounded-sm px-5 pb-2.5 pt-6 dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
      <div className="mb-6 flex items-center justify-between">
        <h4 className="text-xl font-semibold text-black dark:text-white">
          Total: {list.items.length}
        </h4>
          <Link
            href="/"
            className="block w-[100px] rounded border bg-success px-4 text-center font-medium text-white hover:opacity-80 dark:hover:opacity-80 sm:px-4 sm:py-3"
          >
            등록
          </Link>
      </div>
      <div className="max-w-full overflow-x-auto">
        <TableView
          rows={list.items.map((entry, index) => [
            ["번호", index + 1],
            ["키", entry.key],
            ["값", entry.value],
          ])}
        />
      </div>
    </div>
  </section>
}

export default Page;