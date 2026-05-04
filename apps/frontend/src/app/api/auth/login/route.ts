import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { fetchClient } from "@/lib/api/client";
import { cookiesConfig } from "@/lib/api/cookies";

interface T { email: string; password: string }

const POST = async (request: Request) => {
  const body: T = await request.json() as never as T;
  const { data, error, response } = await fetchClient.POST("/auth/login", { body });

  if (error) {
    return NextResponse.json(error, { status: response.status });
  }

  const cookieStore = await cookies();
  cookieStore.set(cookiesConfig.access_cookie_name, data.access_token, cookiesConfig.options);
  cookieStore.set(cookiesConfig.refresh_cookie_name, data.refresh_token, cookiesConfig.options);

  return NextResponse.json({ success: true });
};

export { POST };
