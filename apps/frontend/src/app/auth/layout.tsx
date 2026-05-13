import { Box } from "@/components/ui/layout";

const AuthLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <Box className="flex-1 items-center justify-center">
      {children}
    </Box>
  );
};

export default AuthLayout;
