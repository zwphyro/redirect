import { cookies } from "next/headers";
import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";

import { cookiesConfig } from "./cookies";
import type { paths } from "./v1";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

const createServerClient = async () => {
  const cookieStore = await cookies();
  const token = cookieStore.get(cookiesConfig.access_cookie_name)?.value ?? "";

  const fetchClient = createFetchClient<paths>({
    baseUrl: BACKEND_URL,
  });

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
};

export { createServerClient };
