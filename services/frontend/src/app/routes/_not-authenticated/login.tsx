import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/_not-authenticated/login")({
  component: LoginPage,
});

function LoginPage() {
  return <div>Страница авторизации (Login)</div>;
}
