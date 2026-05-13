import "./globals.css";

import type { Metadata } from "next";
import { Geist_Mono, Inter } from "next/font/google";

import { RootProviders } from "@/app/providers";
import { ApplicationSidebar } from "@/components/sidebar/application-sidebar";
import { Box } from "@/components/ui/layout";
import { cn } from "@/lib/utils";

const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const metadata: Metadata = {
  title: "Redirect",
};

interface RootLayoutProps {
  children: React.ReactNode
}

const RootLayout = ({
  children,
}: RootLayoutProps) => {
  return (
    <html
      lang="en"
      className={cn("h-full antialiased", inter.variable, geistMono.variable)}
      suppressHydrationWarning
    >
      <body className="min-h-full flex flex-col">
        <RootProviders>
          <ApplicationSidebar />
          <Box className="flex-1">
            {children}
          </Box>
        </RootProviders>
      </body>
    </html>
  );
};

export default RootLayout;
export { metadata };
