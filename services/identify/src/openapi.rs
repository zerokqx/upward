use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(
    info(
        title = "Upward Identify Service API",
        version = "0.1.0",
        description = "REST API сервиса идентификации и аутентификации в монорепозитории Upward.\n\n### Возможности сервиса:\n- Аутентификация по email и паролю (Argon2id)\n- Выпуск пар токенов Access (JWT) и Refresh\n- Безопасная ротация Refresh токенов (Token Rotation) с хранением активных сессий в Redis\n- Интеграция с OAuth провайдерами (Google и др.)\n- Проверка работоспособности сервиса (Health Check)",
        contact(
            name = "Upward Team"
        ),
        license(
            name = "MIT"
        )
    ),
    servers(
        (url = "/", description = "Текущий экземпляр сервиса")
    ),
    paths(
        crate::server::health_check,
        crate::login::controller::login_by_password,
        crate::login::controller::register_by_password,
        crate::login::controller::refresh,
        crate::login::controller::get_public_key,
        crate::login::controller::get_public_key_raw,
    ),
    components(
        schemas(
            crate::server::HealthResponseDto,
            crate::login::dto::LoginByPasswordRequestDto,
            crate::login::dto::LoginByPasswordResponseDto,
            crate::login::dto::RegisterRequestDto,
            crate::login::dto::RefreshRequestDto,
            crate::login::dto::PublicKeyResponseDto,
            crate::domain::AccessToken,
            crate::domain::RefreshToken,
        )
    ),
    tags(
        (name = "Health", description = "Проверка состояния и доступности микросервиса"),
        (name = "Auth", description = "Аутентификация, выпуск и ротация токенов доступа")
    )
)]
pub struct ApiDoc;
