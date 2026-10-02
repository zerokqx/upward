import { createRouter, RouterProvider } from "@tanstack/react-router";
import { routeTree } from "../routeTree.gen";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";

const router = createRouter({ routeTree });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

export const TanstackRouterProvider = () => (
  <>
    <RouterProvider router={router} />
    <TanStackRouterDevtools router={router}/>
  </>
);
