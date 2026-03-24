"use client";
import { QueryClientProvider } from "@tanstack/react-query";

import { getQueryClient } from "@/lib/api/query-client";

const Providers = ({ children }: { children: React.ReactNode }) => {
  const queryClient = getQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

export default Providers;
