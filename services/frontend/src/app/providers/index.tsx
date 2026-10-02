import type { ReactNode } from "react";
import { TanstackQueryProvider } from "./tanstack-query";
import { TanstackRouterProvider } from "./tanstack-router";

export const Providers = ({ children }: { children?: ReactNode }) => (
  <TanstackQueryProvider>
  <TanstackRouterProvider />
    {children}
  </TanstackQueryProvider>
);
