"use client";

import { useRouter } from "next/navigation";

import { LoginForm } from "@/components/auth/login-form";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { default as loginContent } from "@/lib/content/auth/login";

const LoginPage = () => {
  const router = useRouter();
  return (
    <Card className="w-96">
      <CardHeader>
        <CardTitle>
          {loginContent.login}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <LoginForm />
      </CardContent>
      <CardFooter>
        <Button variant="link" onClick={() => { router.push("/auth/register"); }}>{loginContent.registerSuggestion}</Button>
      </CardFooter>
    </Card>
  );
};

export default LoginPage;
