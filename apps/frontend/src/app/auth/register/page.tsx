"use client";

import { useRouter } from "next/navigation";

import { RegisterForm } from "@/components/auth/register-form";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { default as registerContent } from "@/lib/content/auth/register";

const RegisterPage = () => {
  const router = useRouter();
  return (
    <Card className="w-96">
      <CardHeader>
        <CardTitle>
          {registerContent.register}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <RegisterForm />
      </CardContent>
      <CardFooter>
        <Button variant="link" onClick={() => { router.push("/auth/login"); }}>{registerContent.loginSuggestion}</Button>
      </CardFooter>
    </Card>
  );
};

export default RegisterPage;
