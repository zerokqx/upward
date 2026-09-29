use axum::extract::{Request, State};
use axum::http::StatusCode;
use axum::middleware::Next;
use axum::response::{IntoResponse, Response};
use jsonwebtoken::{Algorithm, Validation, decode};
use serde::Deserialize;
use uuid::Uuid;

use crate::AppState;
use crate::domain::UserId;

#[derive(Debug, Deserialize)]
struct Claims {
    sub: Uuid,
    exp: usize,
}

pub async fn require_auth(
    State(state): State<AppState>,
    mut request: Request,
    next: Next,
) -> Response {
    let Some(token) = request
        .headers()
        .get(axum::http::header::AUTHORIZATION)
        .and_then(|value| value.to_str().ok())
        .and_then(|value| value.strip_prefix("Bearer "))
    else {
        return StatusCode::UNAUTHORIZED.into_response();
    };

    let mut validation = Validation::new(Algorithm::RS256);
    validation.required_spec_claims.insert("sub".to_string());
    let Ok(data) = decode::<Claims>(token, &state.jwt_key, &validation) else {
        return StatusCode::UNAUTHORIZED.into_response();
    };
    let _ = data.claims.exp;
    request
        .extensions_mut()
        .insert(UserId(data.claims.sub.to_string()));
    next.run(request).await
}
