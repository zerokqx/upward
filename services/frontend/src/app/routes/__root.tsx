import {  createRootRouteWithContext, Link, Outlet } from "@tanstack/react-router";
import type { RouterContext } from "../providers/tanstack-router";
import { AppDevtools } from "../providers";

const RootLayout = () => (
  <>
    <div className="p-2 flex gap-2">
      <Link to="/" className="[&.active]:font-bold">
        Home
      </Link>
    </div>
    <hr />
    <Outlet />
    <AppDevtools />
  </>
);

export const Route = createRootRouteWithContext<RouterContext>()({ component: RootLayout });
