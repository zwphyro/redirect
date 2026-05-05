import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

import { cookiesConfig } from "@/lib/api/cookies";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

const handler = async (request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) => {
  const cookieStore = await cookies();
  const token = cookieStore.get(cookiesConfig.access_cookie_name)?.value;

  const { path } = await params;
  const backendUrl = `${BACKEND_URL}/${path.join("/")}${request.nextUrl.search}`;

  const headers = new Headers(request.headers);
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  headers.delete("host");

  const response = await fetch(backendUrl, {
    method: request.method,
    headers,
    body: request.method !== "GET" && request.method !== "HEAD" ? await request.blob() : undefined,
  });

  return new NextResponse(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: response.headers,
  });
};

export { handler as DELETE, handler as GET, handler as PATCH, handler as POST, handler as PUT };
