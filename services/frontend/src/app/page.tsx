import { dehydrate, HydrationBoundary } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import { getQueryClient } from "@/lib/api/query-client";

import List from "./list";

const Home = async () => {
  const queryClient = getQueryClient();

  await queryClient.prefetchQuery(
    client.queryOptions("get", "/redirect_links/", {
      params: {
        query: {
          limit: 3,
          offset: 0,
        },
      },
    }),
  );

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <List></List>
    </HydrationBoundary>
  );
};

export default Home;
