"use client";

import { useForm } from "@tanstack/react-form";

import { Button } from "@/components/ui/button";
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { useLogin } from "@/lib/api/auth";

const LoginForm = () => {
  const { mutate, isPending, error: loginError } = useLogin();

  const form = useForm({
    defaultValues: {
      email: "",
      password: "",
    },
    onSubmit: ({ value }) => {
      void mutate(value);
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
            const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid;
            return (
              <Field data-invalid={isInvalid}>
                <FieldLabel htmlFor={field.name}>Email</FieldLabel>
                <Input
                  id={field.name}
                  name={field.name}
                  type="email"
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => { field.handleChange(e.target.value); }}
                  aria-invalid={isInvalid}
                  placeholder="me@example.com"
                  autoComplete="email"
                />
                {isInvalid ? <FieldError>{field.state.meta.errors}</FieldError> : null}
              </Field>
            );
          }}
        />
        <form.Field
          name="password"
          children={(field) => {
            const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid || !!loginError;
            return (
              <Field data-invalid={isInvalid}>
                <FieldLabel htmlFor={field.name}>Password</FieldLabel>
                <Input
                  id={field.name}
                  name={field.name}
                  type="password"
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => { field.handleChange(e.target.value); }}
                  aria-invalid={isInvalid}
                  placeholder="********"
                  autoComplete="current-password"
                />
                {isInvalid ?
                  <FieldError>
                    {field.state.meta.errors.length ? field.state.meta.errors : loginError}
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
            Login
          </Button>
        </Field>
      </FieldGroup>
    </form>
  );
};

export default LoginForm;
