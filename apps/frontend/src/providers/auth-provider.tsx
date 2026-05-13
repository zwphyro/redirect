"use client";

import { createContext, type ReactNode, useMemo } from "react";

import { useClient } from "@/lib/api/client";
import type { components } from "@/lib/api/v1";

type User = components["schemas"]["UserSchema"];
type AuthContextValue =
  | { state: "loading", user: null; }
  | { state: "unauthenticated", user: null; }
  | { state: "authenticated", user: User; };

const AuthContext = createContext<AuthContextValue>({
  state: "loading",
  user: null,
});

interface AuthProviderProps {
  children: ReactNode
}

const AuthProvider = ({ children }: AuthProviderProps) => {
  const { client } = useClient();
  const { data: user, isError, isLoading } = client.useQuery(
    "get",
    "/auth/me",
    {},
    {
      retry: false,
    },
  );

  const value: AuthContextValue = useMemo(() => {
    if (isLoading) {
      return { state: "loading", user: null };
    }
    if (isError || !user) {
      return { state: "unauthenticated", user: null };
    }
    return { state: "authenticated", user };
  }, [isLoading, isError, user]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
