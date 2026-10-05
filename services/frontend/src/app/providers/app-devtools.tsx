import { useEffect } from "react";
import { logger } from "@nanostores/logger";
import { TanStackDevtools } from "@tanstack/react-devtools";
import { hotkeysDevtoolsPlugin } from "@tanstack/react-hotkeys-devtools";
import { pacerDevtoolsPlugin } from "@tanstack/react-pacer-devtools";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { $accessToken, $isAuthenticated } from "@/shared/api";

/**
 * Единый компонент инструментов разработки (Devtools).
 * Включает TanStack Devtools, Pacer, Hotkeys, Router Devtools и Nano Stores Logger.
 * В продакшене автоматически возвращает null.
 */
export function AppDevtools() {
  useEffect(() => {
    if (import.meta.env.DEV) {
      return logger({
        "Access Token": $accessToken,
        "Is Authenticated": $isAuthenticated,
      });
    }
  }, []);

  if (!import.meta.env.DEV) {
    return null;
  }

  return (
    <>
      <TanStackDevtools
        eventBusConfig={{
          debug: false,
        }}
        plugins={[pacerDevtoolsPlugin(), hotkeysDevtoolsPlugin()]}
      />
      <TanStackRouterDevtools position="bottom-right" />
    </>
  );
}
