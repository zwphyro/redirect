import type { ElementType, HTMLAttributes } from "react";
import { forwardRef } from "react";

import { cn } from "@/lib/utils";

interface BoxProps extends HTMLAttributes<HTMLDivElement> {
  as?: ElementType;
}

const Box = forwardRef<HTMLDivElement, BoxProps>(
  ({ className, as: Component = "div", ...props }, ref) => {
    return (
      <Component
        ref={ref}
        className={cn("flex min-h-0 min-w-0", className)}
        {...props}
      />
    );
  },
);
Box.displayName = "Box";

const Stack = forwardRef<HTMLDivElement, BoxProps>((props, ref) => (
  <Box
    {...props}
    ref={ref}
    className={cn("flex-col", props.className)}
  />
));
Stack.displayName = "Stack";

const Row = forwardRef<HTMLDivElement, BoxProps>((props, ref) => (
  <Box
    {...props}
    ref={ref}
    className={cn("flex-row items-center", props.className)}
  />
));
Row.displayName = "Row";

export { Box, Row, Stack };
