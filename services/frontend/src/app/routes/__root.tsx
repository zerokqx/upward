import { TanStackDevtools } from "@tanstack/react-devtools";
import { hotkeysDevtoolsPlugin } from "@tanstack/react-hotkeys-devtools";
import { pacerDevtoolsPlugin } from "@tanstack/react-pacer-devtools";
import {  createRootRouteWithContext, Link, Outlet } from "@tanstack/react-router";
import type { RouterContext } from "../providers/tanstack-router";

const RootLayout = () => (
  <>
    <div className="p-2 flex gap-2">
      <Link to="/" className="[&.active]:font-bold">
        Home
      </Link>
    </div>
    <hr />
    <Outlet />
    <TanStackDevtools
      eventBusConfig={{
        debug: false,
      }}
      plugins={[pacerDevtoolsPlugin(), hotkeysDevtoolsPlugin()]}
    />
  </>
);

export const Route = createRootRouteWithContext<RouterContext>()({ component: RootLayout });
