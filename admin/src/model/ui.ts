import { create } from "zustand";

interface DarkModeModel {
  isDark: boolean;
  setIsDark: (value: boolean) => void;
}

export const darkModeModel = create<DarkModeModel>((set) => ({
  isDark: false,
  setIsDark: (value) => set({ isDark: value }),
}));

interface LayoutModel {
  isSidebarOpen: boolean;
  onToggleClick: () => void;
}

export const layoutModel = create<LayoutModel>((set) => ({
  isSidebarOpen: false,
  onToggleClick: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
}));
