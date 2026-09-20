use sqlx::PgPool;

use crate::domain::{SiteId, UserId};

use super::domain::{PingExecution, PingRecord};

#[derive(Clone, Debug)]
pub struct PingRepository {
    pool: PgPool,
}

impl PingRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }

    pub async fn save_ping(
        &self,
        site_id: SiteId,
        ping: &PingExecution,
    ) -> Result<(), sqlx::Error> {
        let extra_json = serde_json::to_value(&ping.extra).unwrap_or(serde_json::Value::Null);
        let duration_ms = ping.ping_duration.as_secs_f64() * 1000.0;

        sqlx::query!(
            r#"
            INSERT INTO site_pings (time, site_id, duration_ms, extra)
            VALUES (NOW(), $1, $2, $3)
            "#,
            site_id.0,
            duration_ms,
            extra_json
        )
        .execute(&self.pool)
        .await?;

        Ok(())
    }

    pub async fn save_pings_batch(&self, results: &[PingRecord]) -> Result<(), sqlx::Error> {
        if results.is_empty() {
            return Ok(());
        }

        let mut query_builder =
            sqlx::QueryBuilder::new("INSERT INTO site_pings (time, site_id, duration_ms, extra) ");

        query_builder.push_values(results, |mut b, item| {
            b.push("NOW()")
                .push_bind(item.site_id.0)
                .push_bind(item.duration_ms)
                .push_bind(&item.extra);
        });

        query_builder.build().execute(&self.pool).await?;

        Ok(())
    }

    pub async fn get_pings(
        &self,
        user_id: &UserId,
        site_id: &SiteId,
    ) -> Result<Vec<PingRecord>, sqlx::Error> {
        let result = sqlx::query_as!(
            PingRecord,
            r#"
            SELECT 
                s.id AS site_id,
                p.duration_ms,
                p.extra
            FROM sites s
            JOIN site_pings p ON p.site_id = s.id
            WHERE s.user_id = $1
              AND s.id = $2
              AND p.time >= NOW() - INTERVAL '30 days'
            ORDER BY p.time DESC
            "#,
            user_id.0,
            site_id.0
        )
        .fetch_all(&self.pool)
        .await?;

        Ok(result)
    }
}
