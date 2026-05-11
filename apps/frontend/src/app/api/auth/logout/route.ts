import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { cookiesConfig } from "@/lib/api/cookies";

export async function POST() {
  const cookieStore = await cookies();
  cookieStore.delete(cookiesConfig.access_cookie_name);
  cookieStore.delete(cookiesConfig.refresh_cookie_name);
  return NextResponse.json({ success: true });
}
