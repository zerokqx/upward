import { createFileRoute, Outlet, redirect } from "@tanstack/react-router";
import { authStorage } from "@/shared/api";
import { authLogger } from "@/shared/lib";

export const Route = createFileRoute("/_not-authenticated")({
  beforeLoad: ({ search, location }) => {
    authLogger.debug("🚪 [Router] Guarding _not-authenticated route", { path: location.pathname });
    if (authStorage.isAuthenticated()) {
      const target = (search as { redirect?: string })?.redirect ?? "/app";
      authLogger.info("🚪 [Router] Already authenticated, redirecting to", { target });
      throw redirect({ to: target });
    }
  },
  component: () => <Outlet />,
});

