use serde::{Deserialize, Serialize, ser};
use std::collections::HashMap;
use std::time::{Duration, Instant};

pub struct UserId(pub String);

#[derive(thiserror::Error, Debug)]
pub enum SiteError {
    #[error("Network Error")]
    Network(#[from] reqwest::Error),

    #[error("Respons from site parse error")]
    InvalidJsonParse(#[from] serde_json::Error),
}

#[derive(Deserialize)]
struct RawPingResponse {
    #[serde(flatten)]
    extra: HashMap<String, serde_json::Value>,
}

#[derive(Debug)]
pub struct PingResponse {
    pub ping_duratation: Duration,
    pub extra: HashMap<String, serde_json::Value>,
}

pub struct Site {
    pub user_id: UserId,
    pub url: String,
}

impl Site {
    pub fn new(url: String, user_id: UserId) -> Self {
        Self { user_id, url }
    }
    pub async fn ping(&self) -> Result<PingResponse, SiteError> {
        let start = Instant::now();
        let result = reqwest::get(&self.url).await?.text().await?;
        let ping_duratation = start.elapsed();
        let parsed_result = serde_json::from_str::<RawPingResponse>(&result)?;
        Ok(PingResponse {
            extra: parsed_result.extra,
            ping_duratation,
        })
    }
}
