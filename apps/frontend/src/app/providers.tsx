"use client";
import { QueryClientProvider } from "@tanstack/react-query";

import { ThemeProvider } from "@/components/themes/theme-provider";
import { getQueryClient } from "@/lib/api/query-client";

const Providers = ({ children }: { children: React.ReactNode }) => {
  const queryClient = getQueryClient();
  return (
    <ThemeProvider>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </ThemeProvider>
  );
};

export { Providers };
