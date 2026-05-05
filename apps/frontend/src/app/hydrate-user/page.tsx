import { dehydrate, HydrationBoundary } from "@tanstack/react-query";

import { getServerClient } from "@/lib/api/client";
import { getQueryClient } from "@/lib/api/query-client";

import HydratedChild from "./hydrated-child";

const RootPage = async () => {
  const queryClient = getQueryClient();
  const { client } = await getServerClient();

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
