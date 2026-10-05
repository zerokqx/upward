import {
  $accessToken,
  $isAuthenticated,
  authEvents,
  authStorage,
  AUTH_EXPIRE_REASON,
} from "./auth-storage";
import { authLogger } from "../lib/logger";

export type AuthBroadcastMessage =
  | { type: "TOKEN_UPDATE"; token: string }
  | { type: "SESSION_EXPIRED" };

const CHANNEL_NAME = "upward_auth_sync";

/**
 * Инициализирует синхронизацию токена и сессии между всеми вкладками браузера через Nano Stores и Nano Events.
 */
export const initAuthBroadcast = (): (() => void) | undefined => {
  if (typeof window === "undefined" || !("BroadcastChannel" in window)) {
    return undefined;
  }

  const channel = new BroadcastChannel(CHANNEL_NAME);
  let isSyncing = false;
  authLogger.debug("📡 [Broadcast] Channel initialized", {
    channel: CHANNEL_NAME,
  });

  // 1. Слушаем события от других вкладок
  channel.onmessage = (event: MessageEvent<AuthBroadcastMessage>) => {
    const message = event.data;
    if (!message || typeof message !== "object") return;

    authLogger.info("📡 [Broadcast] Received event from another tab", message);

    if (message.type === "TOKEN_UPDATE" && message.token) {
      if ($accessToken.get() !== message.token) {
        isSyncing = true;
        try {
          authStorage.setAccessToken(message.token);
        } finally {
          isSyncing = false;
        }
      }
    } else if (message.type === "SESSION_EXPIRED") {
      if ($isAuthenticated.get()) {
        authLogger.info(
          "📡 [Broadcast] Clearing session due to broadcast event from another tab",
        );
        authStorage.clear(AUTH_EXPIRE_REASON.BROADCAST);
      }
    }
  };

  // 2. Отправляем локальные обновления токена (State) в другие вкладки
  const unsubToken = $accessToken.listen((token) => {
    if (!isSyncing && token) {
      authLogger.debug("📡 [Broadcast] Posting TOKEN_UPDATE to other tabs");
      channel.postMessage({ type: "TOKEN_UPDATE", token });
    }
  });

  // 3. Отправляем завершение сессии (Events) в другие вкладки
  const unsubExpired = authEvents.on("session:expired", (reason) => {
    if (reason !== AUTH_EXPIRE_REASON.BROADCAST) {
      authLogger.debug("📡 [Broadcast] Posting SESSION_EXPIRED to other tabs", {
        reason,
      });
      channel.postMessage({ type: "SESSION_EXPIRED" });
    }
  });

  return () => {
    unsubToken();
    unsubExpired();
    channel.close();
    authLogger.debug("📡 [Broadcast] Channel closed");
  };
};

// Автоматическая инициализация в браузере при импорте модуля
export const authBroadcastUnsubscribe = initAuthBroadcast();
