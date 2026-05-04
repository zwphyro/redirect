"use client";

import { useForm } from "@tanstack/react-form";

import { Button } from "@/components/ui/button";
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Stack } from "@/components/ui/layout";
import { client } from "@/lib/api/client";

const RegisterForm = () => {
  const { mutate } = client.useMutation("post", "/auth/register");
  const form = useForm({
    defaultValues: {
      email: "",
      password: "",
      repeatPassword: "",
    },
    onSubmit: (event) => {
      console.log(event);
      const email = event.value.email;
      const password = event.value.password;
      mutate({ body: { email, password } });
    },
  });

  return (
    <Stack className="gap-2">
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
                    autoComplete="false"
                  />
                  {isInvalid ? <FieldError>{field.state.meta.errors}</FieldError> : null}
                </Field>
              );
            }}
          />
          <form.Field
            name="password"
            children={(field) => {
              const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid;
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
                    autoComplete="false"
                  />
                  {isInvalid ? <FieldError>{field.state.meta.errors}</FieldError> : null}
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
                  <FieldLabel htmlFor={field.name}>Repeat Password</FieldLabel>
                  <Input
                    id={field.name}
                    name={field.name}
                    type="password"
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(e) => { field.handleChange(e.target.value); }}
                    aria-invalid={isInvalid}
                    placeholder="********"
                    autoComplete="false"
                  />
                  {isInvalid ? <FieldError>{field.state.meta.errors}</FieldError> : null}
                </Field>
              );
            }}
          />
        </FieldGroup>
      </form>
      <Field>
        <Button type="submit" form="register-form">Register</Button>
      </Field>
    </Stack>
  );
};

export default RegisterForm;
