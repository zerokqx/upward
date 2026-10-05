import { createFileRoute, Outlet, redirect } from "@tanstack/react-router";
import { authStorage, refreshToken } from "@/shared/api";
import { authLogger } from "@/shared/lib";

export const Route = createFileRoute("/_authenticated")({
  beforeLoad: async ({ location }) => {
    authLogger.debug("🛡️ [Router] Guarding _authenticated route", { path: location.pathname });
    if (!authStorage.isAuthenticated()) {
      try {
        await refreshToken();
      } catch {
        // Ошибка рефреша
      }
    }

    // Финальная строгая проверка: если токена в памяти нет — редирект на /login
    if (!authStorage.isAuthenticated()) {
      authLogger.warn("🛡️ [Router] Not authenticated, redirecting to /login", { redirect: location.href });
      throw redirect({
        to: "/login",
        search: {
          redirect: location.href,
        },
      });
    }

    authLogger.info("🛡️ [Router] Access granted to _authenticated route");
  },
  component: () => <Outlet />,
});

