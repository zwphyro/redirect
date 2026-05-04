import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

import { cookiesConfig } from "@/lib/api/cookies";

const handler = async (request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) => {
  const cookieStore = await cookies();
  const token = cookieStore.get(cookiesConfig.access_cookie_name)?.value;

  const { path } = await params;
  const backendUrl = `http://localhost:8000/${path.join("/")}${request.nextUrl.search}`;

  const headers = new Headers(request.headers);
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(backendUrl, {
    method: request.method,
    headers,
    body: request.method !== "GET" ? await request.blob() : undefined,
  });

  return new NextResponse(response.body, {
    status: response.status,
    headers: response.headers,
  });
};

export { handler as DELETE, handler as GET, handler as POST, handler as PUT };
