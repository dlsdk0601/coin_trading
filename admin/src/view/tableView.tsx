import { ReactNode } from "react";

export type TableViewRowItem = [string | ReactNode, ReactNode];
export type TableViewRow = TableViewRowItem[];

export const TableView = (props: { rows: TableViewRow[] }) => {
  return (
    <table className="w-full table-auto">
      <thead>
      <tr className="bg-gray-2 text-left dark:bg-meta-4">
        {(props.rows[0] ?? []).map(([header, _]) => (
          <th
            key={`pagination-header-th-${header}`}
            className="min-w-[220px] px-4 py-4 font-medium text-black dark:text-white xl:pl-11"
          > 
            {header}
          </th>
        ))}
      </tr>
      </thead>
      <tbody>
      {props.rows.map((row) => (
        <tr
          key={`pagination-tbody-tr-${row}`}
          className="hover:bg-gray dark:hover:bg-bodydark1"
        >
          {row.map(([_, data], rowIndex) => (
            <td
              key={rowIndex}
              className="border-b border-[#eee] px-4 py-5 dark:border-strokedark xl:pl-11"
            >
              <span className="text-black dark:text-white">{data}</span>
            </td>
          ))}
        </tr>
      ))}
      </tbody>
    </table>
  );
};