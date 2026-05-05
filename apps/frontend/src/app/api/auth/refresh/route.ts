import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { getServerClient } from "@/lib/api/client";
import { cookiesConfig } from "@/lib/api/cookies";

const POST = async () => {
  const cookieStore = await cookies();
  const refreshToken = cookieStore.get(cookiesConfig.refresh_cookie_name)?.value;

  if (!refreshToken) {
    return NextResponse.json({ error: "No refresh token" }, { status: 401 });
  }

  const { fetchClient } = await getServerClient();

  const { data, error, response } = await fetchClient.POST("/auth/refresh", {
    body: { refresh_token: refreshToken },
  });

  if (error) {
    return NextResponse.json(error, { status: response.status });
  }

  cookieStore.set(cookiesConfig.access_cookie_name, data.access_token, cookiesConfig.options);
  cookieStore.set(cookiesConfig.refresh_cookie_name, data.refresh_token, cookiesConfig.options);

  return NextResponse.json({ success: true });
};

export { POST };
