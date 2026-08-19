import type { Metadata } from "next";
import type { ReactNode } from "react";

import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Internet Atlas",
    template: "%s · Internet Atlas",
  },
  description:
    "A discovery platform for the technology ecosystem. Explore websites, technologies and topics as a connected map.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
