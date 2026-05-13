"use client";

import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Box } from "@/components/ui/layout";

const UnauthenticatedFallback = () => {
  const router = useRouter();

  return (
    <Box className="flex-1 items-center justify-center">
      <Card className="w-96">
        <CardHeader>
          <CardTitle>
            You are not authenticated
          </CardTitle>
          <CardDescription>
            Please log in to continue
          </CardDescription>
        </CardHeader>
        <CardFooter>
          <Button
            className="flex-1"
            onClick={() => { router.push("/auth/login"); }}
          >
            Log in
          </Button>
          <Button
            variant="secondary"
            onClick={() => { router.push("/auth/register"); }}
          >
            Register
          </Button>
        </CardFooter>
      </Card>
    </Box>
  );
};

export { UnauthenticatedFallback };
