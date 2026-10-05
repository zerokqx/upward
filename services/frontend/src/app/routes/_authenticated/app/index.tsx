import { createFileRoute } from "@tanstack/react-router";
import { useStore } from "@nanostores/react";
import {
  $accessToken,
  $isAuthenticated,
  authStorage,
  setMockTokenExpiringIn,
  setMockExpiredToken,
  refreshToken,
} from "@/shared/api";

export const Route = createFileRoute("/_authenticated/app/")({
  component: AppPage,
});

function AppPage() {
  const token = useStore($accessToken);
  const isAuth = useStore($isAuthenticated);

  return (
    <div style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h2>Панель управления Upward (/app)</h2>
      <p>
        <strong>Статус токена:</strong>{" "}
        {isAuth ? "Авторизован ✅" : "Нет токена ❌"}
      </p>
      {token && (
        <p style={{ wordBreak: "break-all", fontSize: 12, color: "#666" }}>
          <strong>JWT Preview:</strong> {token.slice(0, 30)}...
        </p>
      )}

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginTop: 16 }}>
        <button
          type="button"
          onClick={() => setMockTokenExpiringIn(5)}
          style={{ padding: "8px 16px", cursor: "pointer" }}
        >
          ⏱️ Поставить токен (рефреш через 5 сек)
        </button>

        <button
          type="button"
          onClick={() => setMockExpiredToken()}
          style={{ padding: "8px 16px", cursor: "pointer" }}
        >
          ⚠️ Поставить протухший токен
        </button>

        <button
          type="button"
          onClick={() => refreshToken()}
          style={{ padding: "8px 16px", cursor: "pointer" }}
        >
          🔄 Ручной вызов refreshToken()
        </button>

        <button
          type="button"
          onClick={() => authStorage.clear()}
          style={{ padding: "8px 16px", cursor: "pointer", background: "#fee", color: "#c00" }}
        >
          🚪 Выйти (authStorage.clear)
        </button>
      </div>

      <div style={{ marginTop: 20 }}>
        <p style={{ fontSize: 13, color: "#666" }}>
          💡 Откройте консоль браузера (DevTools), чтобы наблюдать за логами <code>tslog</code> в реальном времени!
        </p>
      </div>
    </div>
  );
}

