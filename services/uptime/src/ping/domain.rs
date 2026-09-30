use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use std::time::Duration;

use crate::domain::SiteId;

#[derive(thiserror::Error, Debug)]
pub enum PingError {
    #[error("Probe failed: {0}")]
    Probe(#[from] crate::site::infrastructure::ProbeError),

    #[error("Field '{0}' must be a JSON object")]
    InvalidWidgetField(String),

    #[error("Widget in field '{0}' is missing mandatory 'type' field")]
    MissingWidgetType(String),

    #[error("Widget type in field '{0}' must be a string")]
    InvalidWidgetTypeFormat(String),

    #[error("Unknown widget type '{widget_type}' in field '{field}'")]
    UnknownWidgetType { field: String, widget_type: String },

    #[error("Ping payload cannot be empty")]
    EmptyPayload,

    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
}

/// Валидация структуры пинга и типов виджетов согласно разрешённым в базе данных
pub fn validate_ping_widgets(
    extra: &HashMap<String, serde_json::Value>,
    allowed_types: &HashSet<String>,
) -> Result<(), PingError> {
    if extra.is_empty() {
        return Err(PingError::EmptyPayload);
    }

    for (key, value) in extra {
        let obj = value
            .as_object()
            .ok_or_else(|| PingError::InvalidWidgetField(key.clone()))?;

        let widget_type = obj
            .get("type")
            .ok_or_else(|| PingError::MissingWidgetType(key.clone()))?
            .as_str()
            .ok_or_else(|| PingError::InvalidWidgetTypeFormat(key.clone()))?;

        if !allowed_types.contains(widget_type) {
            return Err(PingError::UnknownWidgetType {
                field: key.clone(),
                widget_type: widget_type.to_string(),
            });
        }
    }

    Ok(())
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

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn sample_allowed_widgets() -> HashSet<String> {
        [
            "badge",
            "stat",
            "gauge",
            "sparkline",
            "key_value",
            "chart",
            "row",
            "column",
            "text",
        ]
        .into_iter()
        .map(String::from)
        .collect()
    }

    #[test]
    fn test_validate_ping_widgets_success() {
        let allowed = sample_allowed_widgets();
        let payload: HashMap<String, serde_json::Value> = serde_json::from_value(json!({
            "status": {
                "type": "badge",
                "label": "App Health",
                "value": "healthy",
                "variant": "success"
            },
            "rps": {
                "type": "stat",
                "label": "Requests / sec",
                "value": 1420,
                "unit": "req/s",
                "trend": 12.4
            },
            "memory": {
                "type": "gauge",
                "label": "RAM Usage",
                "value": 78,
                "max": 100,
                "unit": "%",
                "status": "warning"
            },
            "response_time": {
                "type": "sparkline",
                "label": "Latency (last 10m)",
                "points": [120, 115, 122, 140, 118, 121],
                "unit": "ms"
            },
            "node_info": {
                "type": "key_value",
                "label": "Node Details",
                "data": {
                    "region": "eu-central-1",
                    "version": "v1.4.2",
                    "uptime_hours": 312
                }
            }
        }))
        .unwrap();

        let result = validate_ping_widgets(&payload, &allowed);
        assert!(result.is_ok());
    }

    #[test]
    fn test_validate_ping_widgets_unknown_type() {
        let allowed = sample_allowed_widgets();
        let payload: HashMap<String, serde_json::Value> = serde_json::from_value(json!({
            "cpu": {
                "type": "unsupported_3d_mesh",
                "value": 42
            }
        }))
        .unwrap();

        let result = validate_ping_widgets(&payload, &allowed);
        assert!(matches!(
            result,
            Err(PingError::UnknownWidgetType { field, widget_type })
            if field == "cpu" && widget_type == "unsupported_3d_mesh"
        ));
    }

    #[test]
    fn test_validate_ping_widgets_missing_type() {
        let allowed = sample_allowed_widgets();
        let payload: HashMap<String, serde_json::Value> = serde_json::from_value(json!({
            "status": {
                "label": "App Health"
            }
        }))
        .unwrap();

        let result = validate_ping_widgets(&payload, &allowed);
        assert!(matches!(result, Err(PingError::MissingWidgetType(field)) if field == "status"));
    }

    #[test]
    fn test_validate_ping_widgets_non_object_field() {
        let allowed = sample_allowed_widgets();
        let payload: HashMap<String, serde_json::Value> = serde_json::from_value(json!({
            "status": "healthy"
        }))
        .unwrap();

        let result = validate_ping_widgets(&payload, &allowed);
        assert!(matches!(result, Err(PingError::InvalidWidgetField(field)) if field == "status"));
    }

    #[test]
    fn test_validate_ping_widgets_empty_payload() {
        let allowed = sample_allowed_widgets();
        let payload: HashMap<String, serde_json::Value> = HashMap::new();

        let result = validate_ping_widgets(&payload, &allowed);
        assert!(matches!(result, Err(PingError::EmptyPayload)));
    }
}
