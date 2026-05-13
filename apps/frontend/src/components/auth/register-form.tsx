"use client";

import { useForm } from "@tanstack/react-form";
import { useRouter } from "next/navigation";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { useClient } from "@/lib/api/client";
import { default as registerContent } from "@/lib/content/auth/register";

const registerSchema = z
  .object({
    email: z.email(registerContent.emailInvalid as string),
    password: z
      .string()
      .min(8, registerContent.passwordTooShort)
      .regex(
        /^(?=.*[a-z]).+$/,
        registerContent.passwordLowercase,
      )
      .regex(
        /^(?=.*[A-Z]).+$/,
        registerContent.passwordUppercase,
      )
      .regex(
        /^(?=.*\d).+$/,
        registerContent.passwordNumber,
      ),
    repeatPassword: z.string(),
  })
  .refine(({ password, repeatPassword }) => password === repeatPassword, {
    message: registerContent.repeatPasswordInvalid,
    path: ["repeatPassword"],
  });

const RegisterForm = () => {
  const router = useRouter();
  const { client } = useClient();
  const { mutate, isPending, error: registerError } = client.useMutation("post", "/auth/register");

  const form = useForm({
    defaultValues: {
      email: "",
      password: "",
      repeatPassword: "",
    },
    validators: { onChange: registerSchema },
    onSubmit: (event) => {
      const email = event.value.email;
      const password = event.value.password;
      mutate({ body: { email, password } }, {
        onSuccess: () => { router.push("/auth/login"); },
      });
    },
  });

  return (
    <form
      id="register-form"
      onSubmit={(event: React.SubmitEvent) => {
        event.preventDefault();
        void form.handleSubmit();
      }}
    >
      <FieldGroup>
        <form.Field
          name="email"
          children={(field) => {
            const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid || !!registerError;
            return (
              <Field data-invalid={isInvalid}>
                <FieldLabel htmlFor={field.name}>{registerContent.email}</FieldLabel>
                <Input
                  id={field.name}
                  name={field.name}
                  type="email"
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => { field.handleChange(e.target.value); }}
                  aria-invalid={isInvalid}
                  placeholder={registerContent.emailPlaceholder}
                  autoComplete="false"
                />
                {isInvalid ? <FieldError>{field.state.meta.errors[0]?.message}</FieldError> : null}
              </Field>
            );
          }}
        />
        <form.Field
          name="password"
          children={(field) => {
            const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid || !!registerError;
            return (
              <Field data-invalid={isInvalid}>
                <FieldLabel htmlFor={field.name}>{registerContent.password}</FieldLabel>
                <Input
                  id={field.name}
                  name={field.name}
                  type="password"
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => { field.handleChange(e.target.value); }}
                  aria-invalid={isInvalid}
                  placeholder={registerContent.passwordPlaceholder}
                  autoComplete="false"
                />
                {isInvalid ?
                  <FieldError>
                    {field.state.meta.errors.length
                      ? field.state.meta.errors[0]?.message
                      : registerContent.registerFailedError}
                  </FieldError> : null}
              </Field>
            );
          }}
        />
        <form.Field
          name="repeatPassword"
          children={(field) => {
            const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid;
            return (
              <Field data-invalid={isInvalid}>
                <FieldLabel htmlFor={field.name}>{registerContent.repeatPassword}</FieldLabel>
                <Input
                  id={field.name}
                  name={field.name}
                  type="password"
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => { field.handleChange(e.target.value); }}
                  aria-invalid={isInvalid}
                  placeholder={registerContent.repeatPasswordPlaceholder}
                  autoComplete="false"
                />
                {isInvalid ? <FieldError>{field.state.meta.errors[0]?.message}</FieldError> : null}
              </Field>
            );
          }}
        />
        <Field>
          <Button
            type="submit"
            form="register-form"
            disabled={isPending}
          >
            {registerContent.register}
          </Button>
        </Field>
      </FieldGroup>
    </form>
  );
};

export { RegisterForm };
