import {
  useDocumentVisibility,
  useIdle,
  useWindowEvent,
} from "@siberiacancode/reactuse";
import { authScheduler } from "@/shared/api";
import { authLogger } from "@/shared/lib";

const IDLE_TIMEOUT_MS = 30 * 60 * 1000; // 30 минут простоя

/**
 * Headless-компонент жизненного цикла сессии.
 * Выступает «сенсором» внешних событий браузера:
 * - При простое > 30 минут приостанавливает фоновый планировщик рефреша (useIdle)
 * - При возвращении активности, смене видимости или появлении сети возобновляет проверку токена
 */
export function SessionLifecycle() {
  // 1. Детекция неактивности: если пользователь не двигает мышь/не нажимает клавиши 30 минут
  useIdle(IDLE_TIMEOUT_MS, (idle) => {
    if (idle) {
      authLogger.info(
        "💤 [SessionLifecycle] User became idle for 30m, pausing token refresh",
      );
      authScheduler.pause();
    } else {
      authLogger.info(
        "⚡ [SessionLifecycle] User resumed activity, resuming scheduler",
      );
      authScheduler.resume();
    }
  });

  // 2. Вкладка стала видимой
  useDocumentVisibility((state) => {
    if (state === "visible") {
      authLogger.debug(
        "👀 [SessionLifecycle] Tab became visible, resuming scheduler",
      );
      authScheduler.resume();
    }
  });

  // 3. Сеть снова доступна
  useWindowEvent("online", () => {
    authLogger.debug(
      "🌐 [SessionLifecycle] Network came online, resuming scheduler",
    );
    authScheduler.resume();
  });

  return null;
}
