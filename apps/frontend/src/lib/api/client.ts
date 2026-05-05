import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";

import type { paths } from "./v1";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";
const BROWSER_BASE_URL = "/api/proxy";


const buildServerClient = async () => {
  const { cookies } = await import("next/headers");
  const { cache } = await import("react");
  const { cookiesConfig } = await import("./cookies");

  const createMemoized = cache(async () => {
    const cookieStore = await cookies();
    const token = cookieStore.get(cookiesConfig.access_cookie_name)?.value ?? "";

    const fetchClient = createFetchClient<paths>({ baseUrl: BACKEND_URL });

    fetchClient.use({
      onRequest({ request }) {
        if (token) {
          request.headers.set("Authorization", `Bearer ${token}`);
        }
        return request;
      },
    });

    const client = createClient(fetchClient);
    return { fetchClient, client };
  });

  return createMemoized();
};

const getServerClient = async () => {
  const { cache } = await import("react");
  return cache(() => buildServerClient())();
};


const createBrowserClientSingleton = () => {
  const fetchClient = createFetchClient<paths>({ baseUrl: BROWSER_BASE_URL });

  let refreshPromise: Promise<boolean> | null = null;

  fetchClient.use({
    async onResponse({ response, request, options }) {
      if (response.status === 401) {
        refreshPromise ??= fetch("/api/auth/refresh", { method: "POST" }).then((r) => r.ok);

        const isSuccess = await refreshPromise;
        refreshPromise = null;

        if (isSuccess) {
          return fetch(request.url, options as RequestInit);
        }
        window.location.href = "/auth";
      }
      return response;
    },
  });

  const client = createClient(fetchClient);
  return { fetchClient, client };
};

let browserClientCache: ReturnType<typeof createBrowserClientSingleton> | null = null;

const useClient = () => {
  browserClientCache ??= createBrowserClientSingleton();
  return browserClientCache;
};

export { getServerClient, useClient };
