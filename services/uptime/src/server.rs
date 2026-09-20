use std::net::SocketAddr;
use axum::{Json, Router, http::StatusCode, routing::get};
use serde::Serialize;
use tracing::debug;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

use crate::openapi::ApiDoc;
use crate::{AppState, ping, site};

/// Ответ эндпоинта проверки работоспособности сервиса
#[derive(Serialize, utoipa::ToSchema)]
pub struct HealthResponseDto {
    /// Статус состояния сервиса
    #[schema(example = "ok")]
    pub status: &'static str,

    /// Пояснительное сообщение
    #[schema(example = "Uptime monitoring service is running")]
    pub message: &'static str,
}

/// Проверка работоспособности сервиса (Health Check)
///
/// Возвращает текущее состояние доступности микросервиса.
/// Используется оркестратором (Docker, Kubernetes) для liveness и readiness проб.
#[tracing::instrument]
#[utoipa::path(
    get,
    path = "/health",
    tag = "Health",
    responses(
        (
            status = 200,
            description = "Сервис успешно запущен и обрабатывает запросы",
            body = HealthResponseDto,
            example = json!({
                "status": "ok",
                "message": "Uptime monitoring service is running"
            })
        )
    )
)]
pub async fn health_check() -> (StatusCode, Json<HealthResponseDto>) {
    let response = HealthResponseDto {
        status: "ok",
        message: "Uptime monitoring service is running",
    };
    (StatusCode::OK, Json(response))
}

/// Создание экземпляра Axum приложения со всеми подключенными роутами и состоянием
pub fn create_app(state: AppState) -> Router {
    Router::new()
        .merge(SwaggerUi::new("/docs").url("/docs/docs.json", ApiDoc::openapi()))
        .route("/health", get(health_check))
        .merge(site::routes())
        .merge(ping::routes())
        .with_state(state)
}

/// Запуск HTTP-сервера
pub async fn run_server(
    addr: SocketAddr,
    state: AppState,
) -> Result<(), Box<dyn std::error::Error>> {
    let app = create_app(state);
    let listener = tokio::net::TcpListener::bind(addr).await?;
    debug!("Запускаем сервер на {}", addr);
    axum::serve(listener, app).await?;
    Ok(())
}
