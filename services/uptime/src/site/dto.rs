use serde::{Deserialize, Serialize};

use crate::domain::{SiteId, SiteStatus, SiteUrl, UserId};

/// Данные для регистрации нового сайта в мониторинге
#[derive(Deserialize, Debug, utoipa::ToSchema)]
pub struct CreateSiteDto {
    /// Идентификатор пользователя-владельца
    #[schema(value_type = String, example = "usr_01J8ABCDEF1234567890")]
    pub user_id: UserId,

    /// URL сайта для проверки (поддерживаются только http:// и https://)
    #[schema(value_type = String, example = "https://example.com")]
    pub site: SiteUrl,
}

/// Результат успешного создания сайта
#[derive(Serialize, utoipa::ToSchema)]
pub struct CreateSiteResponseDto {
    /// Идентификатор созданного сайта
    #[schema(value_type = String, example = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11")]
    pub id: SiteId,

    /// Статус операции
    #[schema(example = "pending_verification")]
    pub status: &'static str,

    /// Секретный токен для подтверждения владения сайтом
    #[schema(example = "b428d082-356a-4b92-808c-901a1e582845")]
    pub challenge_token: String,

    /// Путь, по которому должен быть доступен токен
    #[schema(example = "/.well-known/upward")]
    pub challenge_path: &'static str,
}

/// Информация о сайте и статусе его последней проверки (API Response Contract)
#[derive(Serialize, utoipa::ToSchema)]
pub struct SiteResponseDto {
    /// Идентификатор сайта
    #[schema(value_type = String, example = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11")]
    pub id: SiteId,

    /// Идентификатор пользователя-владельца
    #[schema(value_type = String, example = "usr_01J8ABCDEF1234567890")]
    pub user_id: UserId,

    /// Отслеживаемый URL
    #[schema(value_type = String, example = "https://example.com")]
    pub url: SiteUrl,

    /// Время добавления сайта (UTC)
    #[schema(example = "2026-09-15T12:00:00Z")]
    pub created_at: chrono::DateTime<chrono::Utc>,

    /// Время последней проверки (UTC)
    #[schema(example = "2026-09-15T12:05:00Z")]
    pub last_check: Option<chrono::DateTime<chrono::Utc>>,

    /// Текущий статус сайта в очереди (idle, processing)
    #[schema(value_type = String, example = "idle")]
    pub status: SiteStatus,

    /// Время обновления статуса (UTC)
    #[schema(example = "2026-09-15T12:05:00Z")]
    pub status_updated_at: chrono::DateTime<chrono::Utc>,

    /// Дополнительные данные последней проверки (время отклика, заголовки, ошибки)
    #[schema(example = json!({"duration_ms": 142.5}))]
    pub extra: Option<serde_json::Value>,

    /// Признак подтверждения и активности сайта
    #[schema(example = true)]
    pub active: bool,
}
