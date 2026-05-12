const login = {
  login: "Login",
  email: "Email",
  emailInvalid: "Invalid email address",
  emailPlaceholder: "me@example.com",
  password: "Password",
  passwordTooShort: "Password must be at least 8 characters long",
  passwordPlaceholder: "********",
  registerSuggestion: "Don't have an account?",
  getErrorMessage: (status: number) => {
    switch (status) {
      case 401:
        return "Invalid email or password";
      default:
        return "Login failed";
    }
  },
} as const;

export default login;
