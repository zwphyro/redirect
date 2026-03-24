import "./globals.css";
import Providers from "./providers";

import type { Metadata } from "next";

import { cn } from "@/lib/utils";

const metadata: Metadata = {
  title: "Redirect",
};

const RootLayout = ({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) => {
  return (
    <html
      lang="en"
      className={cn("h-full", "antialiased")}
    >
      <body className="min-h-full flex flex-col">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
};

export default RootLayout;
export { metadata };
