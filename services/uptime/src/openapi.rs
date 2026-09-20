use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(
    info(
        title = "Upward Uptime Service API",
        version = "0.1.0",
        description = "REST API сервиса мониторинга доступности сайтов (uptime) в монорепозитории Upward.\n\n### Возможности сервиса:\n- Регистрация сайтов для периодического мониторинга доступности\n- Защита от SSRF (DNS-резолвинг, фильтрация приватных/локальных сетей и проверка по списку запрещённых IP)\n- Фоновый параллельный опрос сайтов с записью метрик в TimescaleDB\n- Получение списка отслеживаемых сайтов и метаданных последних проверок\n- Проверка работоспособности сервиса (Liveness/Readiness probe)",
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
        crate::site::controller::create_site,
        crate::site::controller::get_all_sites,
        crate::site::controller::verify_site,
        crate::ping::controller::get_pings,
    ),
    components(
        schemas(
            crate::server::HealthResponseDto,
            crate::site::dto::CreateSiteDto,
            crate::site::dto::CreateSiteResponseDto,
            crate::site::dto::SiteResponseDto,
            crate::site::dto::VerifySiteResponseDto,
            crate::ping::domain::PingRecord,
            crate::ping::dto::GetPingsDto,
            crate::domain::SiteId,
            crate::domain::UserId,
            crate::domain::SiteUrl,
            crate::domain::SiteStatus,
        )
    ),
    tags(
        (name = "Health", description = "Проверка состояния и доступности микросервиса"),
        (name = "Sites", description = "Регистрация целевых сайтов и получение статусов проверок"),
        (name = "Pings", description = "История и результаты проверок доступности")
    )
)]
pub struct ApiDoc;
