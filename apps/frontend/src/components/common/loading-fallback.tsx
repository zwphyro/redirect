import { Card, CardContent } from "../ui/card";
import { Box } from "../ui/layout";
import { Spinner } from "../ui/spinner";

const LoadingFallback = () => {
  return (
    <Box className="flex-1 items-center justify-center">
      <Card>
        <CardContent>
          <Spinner />
        </CardContent>
      </Card>
    </Box>
  );
};

export { LoadingFallback };
