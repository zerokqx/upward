import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import type { ReactNode } from "react";

// oxlint-disable-next-line react/only-export-components
export const queryClient = new QueryClient();

export const TanstackQueryProvider = ({
  children,
}: {
  children?: ReactNode;
}) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
);
