import { darkModeModel } from "../model/ui";
import { useEffect } from "react";
import { isNil } from "lodash";

const useDarkMode = (): { isDark: boolean; onToggleClick: () => void } => {
  const { isDark, setIsDark } = darkModeModel((state) => state);

  useEffect(() => {
    setIsDark(getTheme());
  }, []);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add("dark");
      document.body.classList.add("dark");
      return;
    }

    document.documentElement.classList.remove("dark");
    document.body.classList.remove("dark");
  }, [isDark]);

  const getTheme = () => {
    if (isNil(localStorage.theme)) {
      return false;
    }

    return (
      localStorage.theme === "dark" || !window.matchMedia("(prefers-color-scheme: dark)").matches
    );
  };

  const onToggleClick = () => {
    const updateMode = !isDark;

    if (updateMode) {
      localStorage.theme = "dark";
    } else {
      localStorage.theme = "light";
    }

    setIsDark(updateMode);
  };

  return { isDark, onToggleClick };
};

export default useDarkMode;
