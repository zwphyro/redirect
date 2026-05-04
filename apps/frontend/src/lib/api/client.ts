import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";

import { isServer } from "@/lib/utils";

import type { paths } from "./v1";


const fetchClient = createFetchClient<paths>({
  baseUrl: "http://dummy",
});

fetchClient.use({
  onRequest({ request }) {
    const url = new URL(request.url);
    const pathWithQuery = url.pathname + url.search;
    const realBase = isServer ? "http://localhost:8000" : "/api/proxy";
    const newUrl = `${realBase}${pathWithQuery}`.replace(/([^:]\/)\/+/g, "$1");
    return new Request(newUrl, request);
  },
});


if (!isServer) {
  let refreshPromise: Promise<boolean> | null = null;
  fetchClient.use({
    async onResponse({ response, request, options }) {
      if (response.status === 401) {
        refreshPromise ??= fetch("/api/auth/refresh", { method: "POST" }).then(r => r.ok);

        const isSuccess = await refreshPromise;
        refreshPromise = null;

        if (isSuccess) {
          return fetch(request.url, options as RequestInit);
        } else {
          window.location.href = "/auth";
        }
      }
      return response;
    },
  });
}

const client = createClient(fetchClient);

export {
  client,
  fetchClient,
};
