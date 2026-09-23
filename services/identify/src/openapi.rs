use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(
    info(
        title = "Upward Identify Service API",
        version = "0.1.0",
        description = "REST API сервиса идентификации и аутентификации в монорепозитории Upward.\n\n### Возможности сервиса:\n- Аутентификация и авторизация пользователей\n- Выпуск и верификация токенов (JWT Ed25519)\n- Публичный эндпоинт открытых ключей (JWKS)\n- Проверка работоспособности сервиса (Liveness/Readiness probe)",
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
    ),
    components(
        schemas(
            crate::server::HealthResponseDto,
        )
    ),
    tags(
        (name = "Health", description = "Проверка состояния и доступности микросервиса")
    )
)]
pub struct ApiDoc;
