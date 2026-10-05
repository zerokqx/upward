import axios, {
  type AxiosError,
  type AxiosRequestConfig,
  type AxiosResponse,
} from "axios";
// import type { AuthResponseDto } from "./bff/model/auth-response-dto";
import { authStorage, AUTH_EXPIRE_REASON } from "./auth-storage";
import { authLogger } from "../lib/logger";
import { createMockJwt } from "./auth-mock";

const BASE_URL =
  (import.meta.env?.VITE_BFF_URL as string) ?? "http://localhost:4000";

let refreshPromise: Promise<string> | null = null;

export const refreshToken = async (): Promise<string> => {
  if (refreshPromise) {
    authLogger.debug("⏳ [Auth] Reusing existing refreshPromise in flight");
    return refreshPromise;
  }

  authLogger.info("🔄 [Auth] Starting token refresh...");

  refreshPromise = (async () => {
    try {
      // === МОК: не делаем запрос к бэкенду, ставим свежий токен ===
      const mockToken = createMockJwt(900);
      authStorage.setAccessToken(mockToken);
      authLogger.info("✅ [Auth] Token refreshed successfully (mock)");
      return mockToken;

      /*
      const response = await axios.post<AuthResponseDto>(
        BASE_URL + "/auth/refresh",
        {},
        { withCredentials: true },
      );
      authStorage.setAccessToken(response.data.access);
      authLogger.info("✅ [Auth] Token refreshed successfully from backend");
      return response.data.access;
      */
    } catch (err) {
      authLogger.error("❌ [Auth] Failed to refresh token:", err);
      authStorage.clear(AUTH_EXPIRE_REASON.REFRESH_FAILED);
      throw err;
    } finally {
      refreshPromise = null;
    }
  })();

  return refreshPromise;
};

export const AXIOS_INSTANCE = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
});

AXIOS_INSTANCE.interceptors.request.use((config) => {
  const token = authStorage.getAccessToken();
  if (token) {
    config.headers.set("Authorization", `Bearer ${token}`);
    authLogger.trace("➡️ [Axios] Request with Bearer token", { url: config.url });
  } else {
    authLogger.trace("➡️ [Axios] Request without token", { url: config.url });
  }
  return config;
});

AXIOS_INSTANCE.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as
      | (AxiosRequestConfig & { _isRetry?: boolean })
      | undefined;

    const isRefreshRequest = originalRequest?.url?.includes("/auth/refresh");

    // 1. Если 401, это не повторный запрос и не сам запрос на рефреш — делаем Silent Retry
    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest._isRetry &&
      !isRefreshRequest
    ) {
      originalRequest._isRetry = true;
      authLogger.warn(
        "🔄 [Axios] 401 received, attempting silent retry with fresh token...",
        { url: originalRequest.url },
      );

      try {
        // Делаем тихий рефреш (с дедупликацией через refreshPromise)
        const newToken = await refreshToken();

        // Обновляем заголовок авторизации в упавшем запросе
        if (originalRequest.headers) {
          if (typeof originalRequest.headers.set === "function") {
            originalRequest.headers.set("Authorization", `Bearer ${newToken}`);
          } else {
            originalRequest.headers["Authorization"] = `Bearer ${newToken}`;
          }
        }

        authLogger.info("🔁 [Axios] Re-executing failed request with new token", {
          url: originalRequest.url,
        });

        // Повторяем оригинальный запрос
        return AXIOS_INSTANCE(originalRequest);
      } catch (refreshErr) {
        authLogger.error(
          "❌ [Axios] Silent retry failed, refresh token is invalid",
          refreshErr,
        );
        return Promise.reject(refreshErr);
      }
    }

    // 2. Если повторный запрос тоже упал с 401 или это сам рефреш — окончательно завершаем сессию
    if (
      error.response?.status === 401 &&
      (!originalRequest || originalRequest._isRetry || isRefreshRequest)
    ) {
      authLogger.warn(
        "⛔ [Axios] 401 Unauthorized cannot be recovered, clearing session",
        { url: originalRequest?.url },
      );
      authStorage.clear(AUTH_EXPIRE_REASON.HTTP_401);
    }

    return Promise.reject(error);
  },
);

export const customInstance = <T>(
  config: AxiosRequestConfig,
  options?: AxiosRequestConfig,
): Promise<T> => {
  return AXIOS_INSTANCE({
    ...config,
    ...options,
  }).then(({ data }: AxiosResponse<T>) => data);
};

export type ErrorType<Error> = AxiosError<Error>;
export type BodyType<BodyData> = BodyData;
