import { AuthGuard } from "@/components/auth/auth-guard";


interface ProtectedLayoutProps {
  children: React.ReactNode
}

const ProtectedLayout = ({
  children,
}: ProtectedLayoutProps) => {
  return (
    <AuthGuard>
      {children}
    </AuthGuard>
  );
};

export default ProtectedLayout;
