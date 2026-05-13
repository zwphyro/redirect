"use client";

import { Stack } from "@/components/ui/layout";
import { useUser } from "@/hooks/use-user";

const ProtectedPage = () => {
  const user = useUser();

  return (
    <Stack>
      <Stack>{JSON.stringify(user, null, 2)}</Stack>
    </Stack>
  );
};

export default ProtectedPage;
