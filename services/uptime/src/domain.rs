use serde::{Deserialize, Serialize};
use std::fmt;

use uuid::Uuid;

/// Идентификатор сайта
#[derive(
    Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize, utoipa::ToSchema, sqlx::Type,
)]
#[sqlx(transparent)]
pub struct SiteId(pub Uuid);

impl fmt::Display for SiteId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl From<Uuid> for SiteId {
    fn from(id: Uuid) -> Self {
        SiteId(id)
    }
}

impl From<SiteId> for Uuid {
    fn from(id: SiteId) -> Self {
        id.0
    }
}

impl std::str::FromStr for SiteId {
    type Err = uuid::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        s.parse::<Uuid>().map(SiteId)
    }
}

/// Идентификатор пользователя-владельца
#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, utoipa::ToSchema, sqlx::Type,
)]
#[sqlx(transparent)]
pub struct UserId(pub String);

impl fmt::Display for UserId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

/// URL сайта
#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, utoipa::ToSchema, sqlx::Type,
)]
#[sqlx(transparent)]
pub struct SiteUrl(pub String);

impl fmt::Display for SiteUrl {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl AsRef<str> for SiteUrl {
    fn as_ref(&self) -> &str {
        &self.0
    }
}

/// Статус состояния сайта в очереди мониторинга
#[derive(
    Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize, utoipa::ToSchema, sqlx::Type,
)]
#[sqlx(type_name = "varchar", rename_all = "snake_case")]
#[serde(rename_all = "snake_case")]
pub enum SiteStatus {
    Idle,
    Processing,
}

impl SiteStatus {
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Idle => "idle",
            Self::Processing => "processing",
        }
    }
}

impl fmt::Display for SiteStatus {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.as_str())
    }
}
