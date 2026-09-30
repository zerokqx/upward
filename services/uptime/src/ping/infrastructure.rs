use std::collections::HashSet;
use std::sync::Arc;
use std::time::Duration;

use sqlx::PgPool;

use super::domain::{PingError, PingExecution, validate_ping_widgets};
use super::repository::PingRepository;
use crate::site::controller::IpValidator;
use crate::site::infrastructure::probe_upward;

#[derive(Clone)]
pub struct HttpPinger {
    pool: PgPool,
    allowed_widgets: Option<Arc<HashSet<String>>>,
}

impl HttpPinger {
    pub fn new(pool: PgPool) -> Self {
        Self {
            pool,
            allowed_widgets: None,
        }
    }

    pub fn with_allowed_widgets(mut self, widgets: Arc<HashSet<String>>) -> Self {
        self.allowed_widgets = Some(widgets);
        self
    }

    pub async fn ping(
        &self,
        url: &str,
        validator: &IpValidator,
    ) -> Result<PingExecution, PingError> {
        let (extra, ping_duration) = probe_upward(url, validator, Duration::from_secs(10)).await?;

        if let Some(allowed) = &self.allowed_widgets {
            validate_ping_widgets(&extra, allowed)?;
        } else {
            let allowed = PingRepository::new(self.pool.clone())
                .get_allowed_widget_types()
                .await?;
            validate_ping_widgets(&extra, &allowed)?;
        }

        Ok(PingExecution {
            ping_duration,
            extra,
        })
    }
}
