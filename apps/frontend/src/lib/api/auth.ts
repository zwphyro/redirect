"use client";

import { useQueryClient } from "@tanstack/react-query";
import { useCallback, useState } from "react";

import { default as loginContent } from "@/lib/content/auth/login";

import type { components } from "./v1";

type LoginBody = components["schemas"]["LoginUserSchema"];
type LoginResponse = components["schemas"]["TokenPairSchema"];
type HttpError = components["schemas"]["HTTPExceptionSchema"];
type ValidationError = components["schemas"]["HTTPValidationError"];

type AuthResult =
  | { ok: true; data: LoginResponse }
  | { ok: false; error: HttpError | ValidationError | string; status: number };

const postLogin = async (body: LoginBody): Promise<AuthResult> => {
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error: HttpError | undefined = await response.json().catch(() => undefined) as never as HttpError | undefined;
    return { ok: false, error: error ?? "Login failed", status: response.status };
  }

  const data: LoginResponse = await response.json() as never as LoginResponse;
  return { ok: true, data };
};

const useLogin = () => {
  const queryClient = useQueryClient();
  const [isPending, setIsPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = useCallback(
    async (
      body: LoginBody,
      options?: { onSuccess?: () => void; onError?: (err: string) => void },
    ) => {
      setIsPending(true);
      setError(null);

      const result = await postLogin(body);
      setIsPending(false);

      if (result.ok) {
        queryClient.removeQueries({ queryKey: ["get", "/auth/me"] });
        options?.onSuccess?.();
      } else {
        const message = loginContent.getErrorMessage(result.status);
        setError(message);
        options?.onError?.(message);
      }

      return result;
    },
    [queryClient],
  );

  const reset = () => {
    setIsPending(false);
    setError(null);
  };

  return { mutate, isPending, error, reset };
};

const postLogout = async () => {
  const response = await fetch("/api/auth/logout", { method: "POST" });
  return { ok: response.ok };
};

const useLogout = () => {
  const queryClient = useQueryClient();

  const mutate = useCallback(
    async (options?: { onSuccess?: () => void }) => {
      await postLogout();
      queryClient.removeQueries({ queryKey: ["get", "/auth/me"] });
      options?.onSuccess?.();
    },
    [queryClient],
  );

  return { mutate };
};

export { useLogin, useLogout };
export type { LoginBody };
