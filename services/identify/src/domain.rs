use derive_more::{Display, From};
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Newtype для Access JWT токена
#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Display, From, ToSchema,
)]
#[serde(transparent)]
#[schema(value_type = String, example = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")]
pub struct AccessToken(pub String);

impl AccessToken {
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl std::ops::Deref for AccessToken {
    type Target = str;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

/// Newtype для Refresh токена
#[derive(
    Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Display, From, ToSchema,
)]
#[serde(transparent)]
#[schema(value_type = String, example = "1024ad10-4b6d-490c-a55d-ed70dcbe4f84")]
pub struct RefreshToken(pub String);

impl RefreshToken {
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl std::ops::Deref for RefreshToken {
    type Target = str;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
