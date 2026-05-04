"use client";

import { Stack } from "@/components/ui/layout";
import { client } from "@/lib/api/client";


const HydratedChild = () => {
  const { data, error, isLoading } = client.useQuery("get", "/auth/me");
  console.log(data, error, isLoading);
  if (isLoading) {
    return <div>Loading...</div>;
  }
  return (
    <Stack>
      <Stack>{JSON.stringify(data, null, 2)}</Stack>
      <Stack>{JSON.stringify(error, null, 2)}</Stack>
    </Stack>
  );
};

export default HydratedChild;
