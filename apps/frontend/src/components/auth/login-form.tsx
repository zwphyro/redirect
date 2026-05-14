"use client";

import { useForm } from "@tanstack/react-form";
import { useRouter } from "next/navigation";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/hooks/use-auth";
import { useLogin } from "@/lib/api/auth";
import { default as loginContent } from "@/lib/content/auth/login";

const loginSchema = z.object({
  email: z.email(loginContent.emailInvalid as string),
  password: z.string().min(8, loginContent.passwordTooShort),
});

const LoginForm = () => {
  const router = useRouter();
  const { refresh } = useAuth();
  const { mutate, isPending, error: loginError, reset } = useLogin();

  const form = useForm({
    defaultValues: {
      email: "",
      password: "",
    },
    validators: { onChange: loginSchema },
    onSubmit: ({ value }) => {
      void mutate(value, {
        onSuccess: () => {
          refresh();
          router.push("/");
        },
      });
    },
  });

  return (
    <form
      id="login-form"
      onSubmit={(event: React.SubmitEvent) => {
        event.preventDefault();
        void form.handleSubmit();
      }}
    >
      <FieldGroup>
        <form.Field
          name="email"
          children={(field) => {
            const isInvalid =
              field.state.meta.isTouched && !field.state.meta.isValid || !!loginError;
            return (
              <Field data-invalid={isInvalid}>
                <FieldLabel htmlFor={field.name}>{loginContent.email}</FieldLabel>
                <Input
                  id={field.name}
                  name={field.name}
                  type="email"
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onFocus={reset}
                  onChange={(e) => { field.handleChange(e.target.value); }}
                  aria-invalid={isInvalid}
                  placeholder={loginContent.emailPlaceholder}
                  autoComplete="email"
                />
                {isInvalid ? <FieldError>{field.state.meta.errors[0]?.message}</FieldError> : null}
              </Field>
            );
          }}
        />
        <form.Field
          name="password"
          children={(field) => {
            const isInvalid =
              field.state.meta.isTouched && !field.state.meta.isValid || !!loginError;
            return (
              <Field data-invalid={isInvalid}>
                <FieldLabel htmlFor={field.name}>{loginContent.password}</FieldLabel>
                <Input
                  id={field.name}
                  name={field.name}
                  type="password"
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onFocus={reset}
                  onChange={(e) => { field.handleChange(e.target.value); }}
                  aria-invalid={isInvalid}
                  placeholder={loginContent.passwordPlaceholder}
                  autoComplete="current-password"
                />
                {isInvalid ?
                  <FieldError>
                    {field.state.meta.errors.length ? field.state.meta.errors[0]?.message : loginError}
                  </FieldError> : null}
              </Field>
            );
          }}
        />
        <Field>
          <Button
            type="submit"
            form="login-form"
            disabled={isPending}
          >
            {loginContent.login}
          </Button>
        </Field>
      </FieldGroup>
    </form>
  );
};

export { LoginForm };
