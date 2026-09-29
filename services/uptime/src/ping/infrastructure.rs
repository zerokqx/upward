use super::domain::{PingError, PingExecution};
use crate::site::controller::IpValidator;
use crate::site::infrastructure::probe_upward;
use std::time::Duration;

#[derive(Clone)]
pub struct HttpPinger {}

impl HttpPinger {
    pub fn new() -> Self {
        Self {}
    }

    pub async fn ping(
        &self,
        url: &str,
        validator: &IpValidator,
    ) -> Result<PingExecution, PingError> {
        let (extra, ping_duration) = probe_upward(url, validator, Duration::from_secs(10)).await?;

        Ok(PingExecution {
            ping_duration,
            extra,
        })
    }
}
