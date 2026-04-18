import { QueryClient } from "@tanstack/react-query";
import createFetchClient from "openapi-fetch";
import createClient from "openapi-react-query";

import type { paths } from "./v1";

const fetchClient = createFetchClient<paths>({
  baseUrl: "http://localhost:8000",
});

const client = createClient(fetchClient);

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
});

export {
  client,
  fetchClient,
  queryClient,
};
