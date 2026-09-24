use argon2::{
    Argon2, PasswordHash, PasswordVerifier,
    password_hash::{Error as ArgonError, PasswordHasher},
};
use axum::extract::State;
use axum::http::StatusCode;
use axum::response::IntoResponse;
use axum::routing::{get, post};
use axum::{Json, Router};

use crate::AppState;
use crate::services::RefreshError;

use super::dto::{
    LoginByPasswordRequestDto, LoginByPasswordResponseDto, PublicKeyResponseDto, RefreshRequestDto,
    RegisterRequestDto,
};

/// Утилита для хеширования и проверки паролей через Argon2id
pub struct ArgonHasher;

impl ArgonHasher {
    /// Хеширует пароль со случайной солью (возвращает ошибку Argon2)
    pub fn hash(password: &str) -> Result<String, ArgonError> {
        let hash = Argon2::default().hash_password(password.as_bytes())?;
        Ok(hash.to_string())
    }

    /// Проверяет совпадение сырого пароля и хеша (возвращает ошибку Argon2)
    pub fn verify(password: &str, hash: &str) -> Result<(), ArgonError> {
        let parsed_hash = PasswordHash::new(hash)?;
        Argon2::default().verify_password(password.as_bytes(), &parsed_hash)
    }
}

/// Аутентификация по email и паролю
///
/// Проверяет учетные данные пользователя (email и пароль), сверяет хеш Argon2
/// и при успехе возвращает пару Access (JWT) и Refresh токенов.
#[utoipa::path(
    post,
    path = "/login/password",
    tag = "Auth",
    request_body(
        content = LoginByPasswordRequestDto,
        description = "Учетные данные пользователя для входа",
        example = json!({
            "email": "user@example.com",
            "password": "strongpassword123"
        })
    ),
    responses(
        (
            status = 200,
            description = "Успешная аутентификация",
            body = LoginByPasswordResponseDto,
            example = json!({
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh": "1024ad10-4b6d-490c-a55d-ed70dcbe4f84"
            })
        ),
        (status = 400, description = "Учетная запись зарегистрирована через OAuth и не имеет пароля"),
        (status = 401, description = "Неверный пароль"),
        (status = 404, description = "Пользователь с указанным email не найден"),
        (status = 500, description = "Внутренняя ошибка сервера")
    )
)]
pub async fn login_by_password(
    State(state): State<AppState>,
    Json(body): Json<LoginByPasswordRequestDto>,
) -> impl IntoResponse {
    let user = state.user_repo.find_by_email(&body.email).await;

    match user {
        Err(_) => StatusCode::INTERNAL_SERVER_ERROR.into_response(),
        Ok(option) => match option {
            Some(user) => match user.password_hash {
                Some(stored_password) => {
                    let raw_password = body.password;

                    let check_result = tokio::task::spawn_blocking(move || {
                        ArgonHasher::verify(&raw_password, &stored_password)
                    })
                    .await;

                    match check_result {
                        Ok(Ok(())) => {
                            let mut redis = state.redis.clone();
                            match state
                                .jwt_service
                                .generate_token_pair(user.id, &user.email, &mut redis)
                                .await
                            {
                                Ok((access, refresh)) => (
                                    StatusCode::OK,
                                    Json(LoginByPasswordResponseDto { access, refresh }),
                                )
                                    .into_response(),
                                Err(_) => StatusCode::INTERNAL_SERVER_ERROR.into_response(),
                            }
                        }
                        Ok(Err(_)) => StatusCode::UNAUTHORIZED.into_response(),
                        Err(_) => StatusCode::INTERNAL_SERVER_ERROR.into_response(),
                    }
                }
                None => StatusCode::BAD_REQUEST.into_response(),
            },
            None => StatusCode::NOT_FOUND.into_response(),
        },
    }
}

/// Обновление пары токенов (Refresh Token Rotation)
///
/// Принимает текущий Refresh токен, проверяет его наличие в Redis,
/// сжигает использованный токен и выпускает новую пару (Access + Refresh).
#[utoipa::path(
    post,
    path = "/refresh",
    tag = "Auth",
    request_body(
        content = RefreshRequestDto,
        description = "Текущий активный Refresh токен",
        example = json!({
            "refresh": "1024ad10-4b6d-490c-a55d-ed70dcbe4f84"
        })
    ),
    responses(
        (
            status = 200,
            description = "Токены успешно обновлены",
            body = LoginByPasswordResponseDto,
            example = json!({
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh": "3209edde-f535-4d07-815e-7070c59e0a37"
            })
        ),
        (status = 401, description = "Невалидный, протухший или повторно использованный Refresh токен"),
        (status = 500, description = "Внутренняя ошибка сервера")
    )
)]
pub async fn refresh(
    State(state): State<AppState>,
    Json(body): Json<RefreshRequestDto>,
) -> impl IntoResponse {
    let mut redis = state.redis.clone();
    match state
        .jwt_service
        .refresh_token_pair(&body.refresh, &state.user_repo, &mut redis)
        .await
    {
        Ok((access, refresh)) => (
            StatusCode::OK,
            Json(LoginByPasswordResponseDto { access, refresh }),
        )
            .into_response(),
        Err(RefreshError::InvalidOrExpiredToken | RefreshError::UserNotFound) => {
            StatusCode::UNAUTHORIZED.into_response()
        }
        Err(_) => StatusCode::INTERNAL_SERVER_ERROR.into_response(),
    }
}

/// Регистрация нового пользователя по email и паролю
#[utoipa::path(
    post,
    path = "/register/password",
    tag = "Auth",
    request_body = RegisterRequestDto,
    responses(
        (status = 201, description = "Пользователь успешно зарегистрирован"),
        (status = 409, description = "Пользователь с таким email уже существует"),
        (status = 500, description = "Внутренняя ошибка сервера")
    )
)]
pub async fn register_by_password(
    State(state): State<AppState>,
    Json(body): Json<RegisterRequestDto>,
) -> Result<impl IntoResponse, StatusCode> {
    if state
        .user_repo
        .find_by_email(&body.email)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?
        .is_some()
    {
        return Err(StatusCode::CONFLICT);
    }

    let password = body.password;
    let password_hash = tokio::task::spawn_blocking(move || ArgonHasher::hash(&password))
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    state
        .user_repo
        .create_user(&body.email, &password_hash)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    Ok(StatusCode::CREATED)
}

/// Получение открытого ключа (RSA Public Key) для локальной верификации JWT в микросервисах
#[utoipa::path(
    get,
    path = "/keys/public",
    tag = "Auth",
    responses(
        (status = 200, description = "Открытый ключ сервиса в формате JSON", body = PublicKeyResponseDto),
    )
)]
pub async fn get_public_key(State(state): State<AppState>) -> impl IntoResponse {
    let response = PublicKeyResponseDto {
        algorithm: "RS256".to_string(),
        public_key: state.jwt_service.public_key_pem().to_string(),
    };
    (StatusCode::OK, Json(response))
}

/// Получение открытого ключа (RSA Public Key) напрямую в формате raw PEM
#[utoipa::path(
    get,
    path = "/keys/public.pem",
    tag = "Auth",
    responses(
        (status = 200, description = "Файл публичного ключа в формате PEM", content_type = "application/x-pem-file"),
    )
)]
pub async fn get_public_key_raw(State(state): State<AppState>) -> impl IntoResponse {
    (
        StatusCode::OK,
        [("content-type", "application/x-pem-file")],
        state.jwt_service.public_key_pem().to_string(),
    )
}

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/login/password", post(login_by_password))
        .route("/register/password", post(register_by_password))
        .route("/refresh", post(refresh))
        .route("/keys/public", get(get_public_key))
        .route("/keys/public.pem", get(get_public_key_raw))
}


