import { cva, type VariantProps } from "class-variance-authority";
import type { ElementType, HTMLAttributes } from "react";
import { forwardRef } from "react";

import { cn } from "@/lib/utils";

const typographyVariants = cva(
  "text-content-primary transition-colors",
  {
    variants: {
      variant: {
        h1: "text-[28px] font-normal leading-tight select-none",
        h2: "text-[24px] font-normal leading-tight select-none",
        h3: "text-[22px] font-normal leading-snug select-none",
        h4: "text-[20px] font-normal leading-snug select-none",
        h5: "text-[18px] font-normal leading-normal select-none",
        h6: "text-[16px] font-normal leading-normal select-none",
        p: "text-[16px] font-normal leading-relaxed",
      },
    },
    defaultVariants: {
      variant: "p",
    },
  },
);

interface TypographyProps
  extends HTMLAttributes<HTMLElement>,
  VariantProps<typeof typographyVariants> {
  as?: ElementType;
}

const Typography = forwardRef<HTMLElement, TypographyProps>(
  ({ className, variant, as, ...props }, ref) => {
    const Component = as ?? variant ?? "p";

    return (
      <Component
        ref={ref}
        className={cn(typographyVariants({ variant, className }))}
        {...props}
      />
    );
  },
);
Typography.displayName = "Typography";

export { Typography, typographyVariants };
