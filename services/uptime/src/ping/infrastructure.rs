use serde::Deserialize;
use std::collections::HashMap;
use std::time::Instant;

use super::domain::{PingError, PingExecution};

#[derive(Deserialize)]
struct RawPingResponse {
    #[serde(flatten)]
    extra: HashMap<String, serde_json::Value>,
}

#[derive(Clone)]
pub struct HttpPinger {
    client: reqwest::Client,
}

impl HttpPinger {
    pub fn new(client: &reqwest::Client) -> Self {
        Self {
            client: client.clone(),
        }
    }

    pub async fn ping(&self, url: &str) -> Result<PingExecution, PingError> {
        let start = Instant::now();
        let result = self.client.get(url).send().await?.text().await?;
        let ping_duration = start.elapsed();
        let parsed_result = serde_json::from_str::<RawPingResponse>(&result)?;

        Ok(PingExecution {
            ping_duration,
            extra: parsed_result.extra,
        })
    }
}
