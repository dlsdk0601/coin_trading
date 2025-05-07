import React from "react";
import type { Metadata } from "next";
import "../../public/css/satoshi.css";
import "../../public/css/icons.css";
import "../../public/css/globals.css";

export const metadata: Metadata = {
  title: "admin",
  description: "portfolio admin for ina",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="sidebar-expanded">{children}</body>
    </html>
  );
}
