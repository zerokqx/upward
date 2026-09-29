use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::Duration;

use crate::domain::SiteId;

#[derive(thiserror::Error, Debug)]
pub enum PingError {
    #[error("Probe failed: {0}")]
    Probe(#[from] crate::site::infrastructure::ProbeError),
}

/// Результат единичного сетевого замера доступности
#[derive(Debug, Clone)]
pub struct PingExecution {
    pub ping_duration: Duration,
    pub extra: HashMap<String, serde_json::Value>,
}

/// Запись замера доступности, подготовленная для сохранения в базу данных
#[derive(Debug, Clone, Serialize, Deserialize, utoipa::ToSchema)]
pub struct PingRecord {
    pub site_id: SiteId,
    pub duration_ms: f64,
    pub extra: serde_json::Value,
}
