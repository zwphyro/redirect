const isProduction = process.env.NODE_ENV === "production";

const cookiesConfig = {
  access_cookie_name: isProduction ? "__Host-access-token" : "access_token",
  refresh_cookie_name: isProduction ? "__Host-refresh-token" : "refresh_token",
  options: {
    httpOnly: true,
    secure: isProduction,
    sameSite: "lax",
    path: "/",
  },
} as const;

export { cookiesConfig };
