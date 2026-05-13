import { LayoutPanelLeftIcon, SettingsIcon } from "lucide-react";

import { Sidebar, SidebarContent, SidebarFooter, SidebarGroup, SidebarMenu, SidebarMenuBadge, SidebarMenuButton, SidebarMenuItem } from "@/components/ui/sidebar";

import { UserSection } from "./user-section";


const ApplicationSidebar = () => {
  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton>
                <LayoutPanelLeftIcon />
                Dashboard
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>

          <SidebarMenuItem>
            <SidebarMenuButton>
              Settings
            </SidebarMenuButton>
            <SidebarMenuBadge>
              <SettingsIcon size={16} />
            </SidebarMenuBadge>
          </SidebarMenuItem>


          <UserSection />
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
};

export { ApplicationSidebar };
