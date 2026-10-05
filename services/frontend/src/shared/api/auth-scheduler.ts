import { jwtDecode, type JwtPayload } from "jwt-decode";
import { $accessToken, authStorage, DEFAULT_BUFFER_SECS } from "./auth-storage";
import { refreshToken } from "./axios-client";
import { authLogger } from "../lib/logger";

let refreshTimeout: ReturnType<typeof setTimeout> | null = null;
let isPaused = false;

/**
 * Агностичный планировщик превентивного обновления токена.
 * Управляет таймером setTimeout вне дерева React и вне HTTP-клиента.
 */
export const authScheduler = {
  /**
   * Запланировать превентивное обновление токена до его истечения
   */
  schedule: (
    token: string | null = authStorage.getAccessToken(),
    bufferSecs = DEFAULT_BUFFER_SECS,
  ): void => {
    authScheduler.clear();

    if (!token) return;
    if (isPaused) {
      authLogger.debug("⏸️ [Scheduler] Schedule skipped: scheduler is paused");
      return;
    }

    try {
      const { exp } = jwtDecode<JwtPayload>(token);
      if (!exp) return;

      const delayMs = (exp - bufferSecs) * 1000 - Date.now();

      if (delayMs > 0) {
        authLogger.debug(
          `⏱️ [Scheduler] Next refresh in ${Math.round(delayMs / 1000)}s`,
          { delayMs, exp },
        );
        refreshTimeout = setTimeout(() => {
          refreshToken().catch(() => {});
        }, delayMs);
      } else {
        authLogger.warn(
          "⚠️ [Scheduler] Token expired or delay <= 0, refreshing immediately",
          { delayMs },
        );
        refreshToken().catch(() => {});
      }
    } catch (err) {
      authLogger.error("❌ [Scheduler] Failed to decode token", err);
    }
  },

  /**
   * Поставить планировщик на паузу (например, при простое пользователя > 30 минут)
   */
  pause: (): void => {
    isPaused = true;
    authScheduler.clear();
    authLogger.info("⏸️ [Scheduler] Refresh paused (user is idle / inactive)");
  },

  /**
   * Снять с паузы и при необходимости обновить токен (при пробуждении, фокусе или сети)
   */
  resume: (): void => {
    isPaused = false;
    authLogger.info("▶️ [Scheduler] Resumed, verifying token freshness");

    if (authStorage.isExpiredAccessToken()) {
      authLogger.warn("⚠️ [Scheduler] Token expired while paused, refreshing now");
      refreshToken().catch(() => {});
    } else {
      authScheduler.schedule();
    }
  },

  /**
   * Очистить текущий таймер
   */
  clear: (): void => {
    if (refreshTimeout) {
      clearTimeout(refreshTimeout);
      refreshTimeout = null;
      authLogger.debug("🛑 [Scheduler] Cleared refresh timer");
    }
  },

  isPaused: (): boolean => isPaused,
};

// Автоматическая реакция на изменение токена в памяти
$accessToken.listen((token) => {
  if (token) {
    authScheduler.schedule(token);
  } else {
    authScheduler.clear();
  }
});
