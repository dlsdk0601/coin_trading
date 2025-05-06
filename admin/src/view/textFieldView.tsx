import classNames from "classnames";
import { isNil } from "lodash";
import { ReactNode } from "react";
import { isBlank, isNotBlank, isNotNil } from "../ex/utils";

const TextFieldView = (props: {
  name: string;
  label?: string;
  placeholder?: string;
  icon?: ReactNode;
  col?: 2 | 3;
  type?: "text" | "password" | "email" | "tel";
  error?: string;
}) => {
  return (
    <div
      className={classNames("mb-5.5 w-full", {
        "sm:w-1/2": props.col === 2,
        "sm:w-1/3": props.col === 3,
      })}
    >
      <label className="mb-2.5 block text-sm font-medium text-black dark:text-white">
        {props.label ?? props.name}
      </label>
      <div className="relative">
        {props.icon}
        <input
          type={props.type ?? "text"}
          className={classNames(
            "dark:bg-meta-4 dark:focus:border-primary w-full rounded border py-3 pr-4.5 text-black focus-visible:outline-none dark:text-white",
            {
              "pl-11.5": isNotNil(props.icon),
              "pl-6": isNil(props.icon),
              "border-meta-1 focus:border-meta-1": isNotBlank(props.error),
              "border-stroke focus:border-primary": isBlank(props.error),
            },
          )}
          name={props.name}
          placeholder={props.placeholder}
        />
      </div>
      {isNotBlank(props.error) && <p className="text-meta-1 mt-1 text-xs italic">{props.error}</p>}
    </div>
  );
};

export default TextFieldView;
