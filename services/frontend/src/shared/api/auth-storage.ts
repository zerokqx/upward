import { atom, computed } from "nanostores";
import { createNanoEvents } from "nanoevents";
import { jwtDecode, type JwtPayload } from "jwt-decode";
import { authLogger } from "../lib/logger";

/**
 * Причины завершения сессии (object as const + type)
 */
export const AUTH_EXPIRE_REASON = {
  MANUAL: "manual",
  HTTP_401: "401",
  BROADCAST: "broadcast",
  REFRESH_FAILED: "refresh_failed",
} as const;

export type AuthExpireReason =
  (typeof AUTH_EXPIRE_REASON)[keyof typeof AUTH_EXPIRE_REASON];

/**
 * 1. ИВЕНТЫ (Nano Events) — шина жизненного цикла сессии
 */
export interface AuthEvents {
  "session:expired": (reason: AuthExpireReason) => void;
}

export const authEvents = createNanoEvents<AuthEvents>();

/**
 * 2. СТЕЙТ (Nano Stores) — реактивное хранение токена
 */
export const $accessToken = atom<string | null>(null);

/**
 * Вычисляемый статус авторизации
 */
export const $isAuthenticated = computed($accessToken, (token) => token !== null);

export const DEFAULT_BUFFER_SECS = 60;

/**
 * Проверка срока годности токена
 */
export const isExpiredToken = (
  token: string | null = $accessToken.get(),
  bufferSecs = DEFAULT_BUFFER_SECS,
): boolean => {
  if (!token) return true;
  try {
    const { exp } = jwtDecode<JwtPayload>(token);
    if (!exp) return true;
    return Date.now() >= (exp - bufferSecs) * 1000;
  } catch {
    return true;
  }
};

// Логирование изменений стейта и событий через tslog
$accessToken.listen((token) => {
  if (token) {
    authLogger.info("🔑 [State:$accessToken] Token updated");
  } else {
    authLogger.info("🔒 [State:$accessToken] Token is null");
  }
});

authEvents.on("session:expired", (reason) => {
  authLogger.warn("🚪 [Event:session:expired] Session terminated", { reason });
});

/**
 * 3. Удобный фасад для мутаций и проверок
 */
export const authStorage = {
  getAccessToken: () => $accessToken.get(),
  setAccessToken: (token: string | null) => {
    const cleanToken = token?.trim() || null;
    $accessToken.set(cleanToken);
  },
  clear: (reason: AuthExpireReason = AUTH_EXPIRE_REASON.MANUAL) => {
    $accessToken.set(null);
    authEvents.emit("session:expired", reason);
  },
  isAuthenticated: () => $isAuthenticated.get(),
  isExpiredAccessToken: (bufferSecs = DEFAULT_BUFFER_SECS) =>
    isExpiredToken($accessToken.get(), bufferSecs),
};
