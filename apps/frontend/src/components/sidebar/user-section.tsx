"use client";

import { LogOutIcon } from "lucide-react";
import { useRouter } from "next/navigation";

import { useAuth } from "@/hooks/use-auth";
import { useLogout } from "@/lib/api/auth";

import { Button } from "../ui/button";
import { SidebarMenuAction, SidebarMenuButton, SidebarMenuItem, SidebarMenuSkeleton } from "../ui/sidebar";

const UserSection = () => {
  const { mutate } = useLogout();
  const router = useRouter();
  const { state, user } = useAuth();

  if (state === "loading") {
    return (
      <SidebarMenuSkeleton />
    );
  }

  if (state !== "authenticated") {
    return (
      <SidebarMenuItem className="flex">
        <Button
          className="flex-1"
          onClick={() => { router.push("/auth/login"); }}
        >
          Log in
        </Button>
        <Button
          className="flex-1"
          variant="secondary"
          onClick={() => { router.push("/auth/register"); }}
        >
          Register
        </Button>
      </SidebarMenuItem>
    );
  }

  return (
    <SidebarMenuItem>
      <SidebarMenuButton>
        {user.email}
      </SidebarMenuButton>
      <SidebarMenuAction
        onClick={() => { void mutate({ onSuccess: () => { router.push("/auth/login"); } }); }}
      >
        <LogOutIcon />
      </SidebarMenuAction>
    </SidebarMenuItem>
  );
};

export { UserSection };
