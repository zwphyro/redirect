import { dehydrate, HydrationBoundary } from "@tanstack/react-query";
import { cookies } from "next/headers";

import { client } from "@/lib/api/client";
import { cookiesConfig } from "@/lib/api/cookies";
import { getQueryClient } from "@/lib/api/query-client";

import HydratedChild from "./hydrated-child";


const RootPage = async () => {
  const queryClient = getQueryClient();
  const cookieStore = await cookies();
  const token = cookieStore.get(cookiesConfig.access_cookie_name)?.value ?? "";
  await queryClient.prefetchQuery(
    client.queryOptions("get", "/auth/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: {},
    }),
  );
  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <HydratedChild />
    </HydrationBoundary>
  );
};

export default RootPage;
