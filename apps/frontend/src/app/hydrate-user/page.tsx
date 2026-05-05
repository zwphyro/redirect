import { dehydrate, HydrationBoundary } from "@tanstack/react-query";

import { getQueryClient } from "@/lib/api/query-client";
import { createServerClient } from "@/lib/api/server-client";

import HydratedChild from "./hydrated-child";

const RootPage = async () => {
  const queryClient = getQueryClient();
  const { client } = await createServerClient();

  await queryClient.prefetchQuery(
    client.queryOptions("get", "/auth/me"),
  );

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <HydratedChild />
    </HydrationBoundary>
  );
};

export default RootPage;
