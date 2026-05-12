import login from "./login";
import register from "./register";

const auth = {
  login: login,
  register: register,
} as const;

export default auth;
