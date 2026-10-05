import { authStorage } from "./auth-storage";
import { authLogger } from "../lib/logger";

const BUFFER_SECS = 60;

/**
 * Генерация валидного mock JWT для локального тестирования без бэкенда.
 */
export const createMockJwt = (lifetimeSecs = 900): string => {
  const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const now = Math.floor(Date.now() / 1000);
  const payload = btoa(
    JSON.stringify({
      sub: "mock-user-123",
      email: "mock@upward.dev",
      iat: now,
      exp: now + lifetimeSecs,
    }),
  );
  return `${header}.${payload}.mock_signature`;
};

/**
 * Эмуляция: ставит токен, у которого рефреш сработает через `seconds` секунд.
 */
export const setMockTokenExpiringIn = (seconds = 5): string => {
  authLogger.warn(
    `🧪 [Mock] Setting token that triggers proactive refresh in ${seconds}s`,
  );
  const token = createMockJwt(BUFFER_SECS + seconds);
  authStorage.setAccessToken(token);
  return token;
};

/**
 * Эмуляция: ставит уже полностью протухший токен.
 */
export const setMockExpiredToken = (): string => {
  authLogger.warn("🧪 [Mock] Setting expired token (exp in past)");
  const token = createMockJwt(-60);
  authStorage.setAccessToken(token);
  return token;
};
