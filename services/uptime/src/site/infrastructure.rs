use std::collections::HashMap;
use std::time::Instant;
use serde::Deserialize;

use super::domain::{PingResponse, Site, SiteError};

#[derive(Deserialize)]
struct RawPingResponse {
    #[serde(flatten)]
    extra: HashMap<String, serde_json::Value>,
}

#[derive(Clone)]
pub struct SitePinger {
    client: reqwest::Client,
}

impl SitePinger {
    pub fn new(client: &reqwest::Client) -> Self {
        Self {
            client: client.clone(),
        }
    }

    pub async fn ping(&self, site: &Site) -> Result<PingResponse, SiteError> {
        let start = Instant::now();
        let result = self.client.get(&site.url).send().await?.text().await?;
        let ping_duration = start.elapsed();
        let parsed_result = serde_json::from_str::<RawPingResponse>(&result)?;

        Ok(PingResponse {
            ping_duration,
            extra: parsed_result.extra,
        })
    }
}
