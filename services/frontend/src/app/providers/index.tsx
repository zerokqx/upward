import type { ReactNode } from "react";
import { TanstackQueryProvider } from "./tanstack-query";
import { TanstackRouterProvider } from "./tanstack-router";
import { SessionLifecycle } from "@/entities/session";

export const Providers = ({ children }: { children?: ReactNode }) => (
  <TanstackQueryProvider>
    <SessionLifecycle />
    <TanstackRouterProvider />
    {children}
  </TanstackQueryProvider>
);

export { AppDevtools } from "./app-devtools";

