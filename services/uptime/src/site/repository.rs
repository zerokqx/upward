use sqlx::PgPool;

use super::domain::{PingResponse, Site};

pub struct SiteRepository {
    pool: PgPool,
}

impl SiteRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
    pub async fn save_site(&self, site: &Site) -> Result<i64, sqlx::Error> {
        let row: (i64,) =
            sqlx::query_as("INSERT INTO sites (user_id, url) VALUES ($1, $2) RETURNING id")
                .bind(&site.user_id.0)
                .bind(&site.url)
                .fetch_one(&self.pool)
                .await?;
        Ok(row.0)
    }
    pub async fn save_ping(&self, site_id: i64, ping: &PingResponse) -> Result<(), sqlx::Error> {
        let extra_json = serde_json::to_value(&ping.extra).unwrap_or(serde_json::Value::Null);
        let duration_ms = ping.ping_duratation.as_secs_f64() * 1000.0;

        sqlx::query(
            r#"
            INSERT INTO site_pings (time, site_id, duration_ms, extra)
            VALUES (NOW(), $1, $2, $3)
            "#,
        )
        .bind(site_id)
        .bind(duration_ms)
        .bind(extra_json)
        .execute(&self.pool)
        .await?;

        Ok(())
    }
}
