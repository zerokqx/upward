import { createRouter, RouterProvider } from "@tanstack/react-router";
import { routeTree } from "../routeTree.gen";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { queryClient } from "./tanstack-query";
import type { QueryClient } from "@tanstack/react-query";

export interface RouterContext {
  readonly queryClient: QueryClient;
}
const router = createRouter({ routeTree, context: { queryClient } });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

export const TanstackRouterProvider = () => (
  <>
    <RouterProvider router={router} />
    <TanStackRouterDevtools router={router} />
  </>
);
