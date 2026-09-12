use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::Duration;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct UserId(pub String);

#[derive(thiserror::Error, Debug)]
pub enum SiteError {
    #[error("Network Error: {0}")]
    Network(#[from] reqwest::Error),

    #[error("Response from site parse error: {0}")]
    InvalidJsonParse(#[from] serde_json::Error),
}

#[derive(Debug, Clone)]
pub struct PingResponse {
    pub ping_duration: Duration,
    pub extra: HashMap<String, serde_json::Value>,
}

#[derive(Debug, Clone)]
pub struct PingResult {
    pub site_id: i64,
    pub duration_ms: f64,
    pub extra: serde_json::Value,
}

#[derive(Debug, Clone)]
pub struct Site {
    pub id: Option<i64>,
    pub user_id: UserId,
    pub url: String,
}

impl Site {
    pub fn new(url: String, user_id: UserId) -> Self {
        Self {
            id: None,
            user_id,
            url,
        }
    }

    pub fn with_id(id: i64, url: String, user_id: UserId) -> Self {
        Self {
            id: Some(id),
            user_id,
            url,
        }
    }
}
