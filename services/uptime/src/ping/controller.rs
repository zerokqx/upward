use axum::Json;
use axum::extract::{Path, Query, State};
use axum::http::StatusCode;
use axum::routing::{Router, get};

use crate::AppState;
use crate::domain::SiteId;
use super::domain::PingRecord;
use super::dto::GetPingsDto;

#[tracing::instrument(skip(state))]
#[utoipa::path(
    get,
    path = "/sites/{site_id}/pings",
    tag = "Pings",
    params(
        ("site_id" = uuid::Uuid, Path, description = "Идентификатор сайта"),
        GetPingsDto
    ),
    responses(
        (
            status = 200,
            description = "История проверок доступности сайта за последние 30 дней",
            body = Vec<PingRecord>
        ),
        (
            status = 500,
            description = "Внутренняя ошибка сервера при чтении из базы данных",
            body = String
        )
    )
)]
pub async fn get_pings(
    State(state): State<AppState>,
    Path(site_id): Path<SiteId>,
    Query(query): Query<GetPingsDto>,
) -> Result<Json<Vec<PingRecord>>, (StatusCode, String)> {
    let pings = state
        .ping_repo
        .get_pings(&query.user_id, &site_id)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    Ok(Json(pings))
}

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/sites/{site_id}/pings", get(get_pings))
}
