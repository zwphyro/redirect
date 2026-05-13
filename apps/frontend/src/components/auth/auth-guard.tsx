"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";

import { useAuth } from "@/hooks/use-auth";

import { LoadingFallback } from "../common/loading-fallback";
import { UnauthenticatedFallback } from "./unathenticated-fallback";

const AuthGuard = ({ children }: { children: React.ReactNode }) => {
  const { state } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    if (state === "unauthenticated" && pathname !== "/") {
      router.push("/");
    }
  }, [state, pathname, router]);

  if (state === "loading") {
    return <LoadingFallback />;
  }

  if (state === "unauthenticated") {
    if (pathname === "/") {
      return <UnauthenticatedFallback />;
    }
    return null;
  }

  return <>{children}</>;
};

export { AuthGuard };
