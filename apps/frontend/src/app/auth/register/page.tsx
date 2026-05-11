import RegisterForm from "@/components/auth/RegisterForm";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const RegisterPage = () => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>
          Register
        </CardTitle>
      </CardHeader>
      <CardContent>
        <RegisterForm />
      </CardContent>
    </Card>
  );
};

export default RegisterPage;
