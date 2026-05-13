import { useAuth } from "@/hooks/use-auth";

const useUser = () => {
  const { state, user } = useAuth();

  if (state !== "authenticated") {
    throw new Error("Not authenticated");
  }

  return user;
};

export { useUser };
