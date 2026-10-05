import { createFileRoute, redirect } from "@tanstack/react-router";
import { authStorage, refreshToken } from "@/shared/api";
import { authLogger } from "@/shared/lib";

export const Route = createFileRoute("/")({
  beforeLoad: async () => {
    authLogger.debug("🏠 [Router] Checking root index route");
    if (!authStorage.isAuthenticated()) {
      try {
        await refreshToken();
      } catch {
        authLogger.debug("🏠 [Router] Guest user on index page");
        return;
      }
    }

    if (authStorage.isAuthenticated()) {
      authLogger.info("🏠 [Router] User authenticated, redirecting to /app");
      throw redirect({ to: "/app" });
    }
  },
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/"! (Публичный лендинг)</div>;
}

