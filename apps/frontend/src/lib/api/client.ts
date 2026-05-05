import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";

import type { paths } from "./v1";

const fetchClient = createFetchClient<paths>({
  baseUrl: "/api/proxy",
});

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

export { client, fetchClient };
