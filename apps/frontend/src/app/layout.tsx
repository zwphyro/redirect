import "./globals.css";

import type { Metadata } from "next";

import { cn } from "@/lib/utils";

import { Providers } from "./providers";

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
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
};

export default RootLayout;
export { metadata };
