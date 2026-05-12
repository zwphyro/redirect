const register = {
  register: "Register",
  email: "Email",
  emailInvalid: "Invalid email address",
  emailPlaceholder: "me@example.com",
  password: "Password",
  passwordTooShort: "Password must be at least 8 characters long",
  passwordLowercase: "Password must contain at least one lowercase letter",
  passwordUppercase: "Password must contain at least one uppercase lerrer",
  passwordNumber: "Password must contain at least one number",
  passwordPlaceholder: "********",
  repeatPassword: "Repeat password",
  repeatPasswordInvalid: "Passwords do not match",
  repeatPasswordPlaceholder: "********",
  registerFailedError: "Registration failed",
  loginSuggestion: "Already have an account?",
} as const;

export default register;
