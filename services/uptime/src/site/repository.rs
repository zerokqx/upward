use sqlx::PgPool;

use super::domain::{PingResponse, Site, UserId};

#[derive(Clone)]
pub struct SiteRepository {
    pool: PgPool,
}

impl SiteRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
    pub async fn save_site(&self, site: &Site) -> Result<i64, sqlx::Error> {
        let res = sqlx::query!(
            r#"
        INSERT INTO sites (user_id, url)
        VALUES ($1, $2)
        RETURNING id
        "#,
            site.user_id.0,
            site.url
        )
        .fetch_one(&self.pool)
        .await;

        match res {
            Ok(record) => Ok(record.id),
            Err(err) => {
                if let Some(db_err) = err.as_database_error() {
                    if db_err.code() == Some("23505".into()) {
                        println!("Попытка дублирования сайта: {}", site.url);
                    }
                }
                Err(err)
            }
        }
    }
    pub async fn get_sites_for_ping(&self, limit: i64) -> Result<Vec<Site>, sqlx::Error> {
        let records = sqlx::query!(
            r#"
            WITH target_sites AS (
                SELECT id
                FROM sites
                WHERE (status = 'idle' AND (last_check IS NULL OR last_check < NOW() - INTERVAL '60 seconds'))
                   OR (status = 'processing' AND status_updated_at < NOW() - INTERVAL '3 minutes')
                ORDER BY last_check ASC NULLS FIRST
                LIMIT $1
                FOR UPDATE SKIP LOCKED
            )
            UPDATE sites s
            SET status = 'processing',
                status_updated_at = NOW()
            FROM target_sites ts
            WHERE s.id = ts.id
            RETURNING s.id, s.url, s.user_id
            "#,
            limit
        )
        .fetch_all(&self.pool)
        .await?;

        let sites = records
            .into_iter()
            .map(|r| Site::with_id(r.id, r.url, UserId(r.user_id)))
            .collect();

        Ok(sites)
    }
    pub async fn save_ping(&self, site_id: i64, ping: &PingResponse) -> Result<(), sqlx::Error> {
        let extra_json = serde_json::to_value(&ping.extra).unwrap_or(serde_json::Value::Null);
        let duration_ms = ping.ping_duration.as_secs_f64() * 1000.0;

        sqlx::query!(
            r#"
            INSERT INTO site_pings (time, site_id, duration_ms, extra)
            VALUES (NOW(), $1, $2, $3)
            "#,
            site_id,
            duration_ms,
            extra_json
        )
        .execute(&self.pool)
        .await?;

        Ok(())
    }

    pub async fn save_pings_batch(
        &self,
        results: &[crate::site::domain::PingResult],
    ) -> Result<(), sqlx::Error> {
        if results.is_empty() {
            return Ok(());
        }

        let mut tx = self.pool.begin().await?;

        // 1. Пакетная вставка всех пингов за 1 запрос
        let mut query_builder =
            sqlx::QueryBuilder::new("INSERT INTO site_pings (time, site_id, duration_ms, extra) ");

        query_builder.push_values(results, |mut b, item| {
            b.push("NOW()")
                .push_bind(item.site_id)
                .push_bind(item.duration_ms)
                .push_bind(&item.extra);
        });

        query_builder.build().execute(&mut *tx).await?;

        // 2. Пакетное обновление статуса сайтов обратно в idle
        let site_ids: Vec<i64> = results.iter().map(|r| r.site_id).collect();

        sqlx::query!(
            r#"
            UPDATE sites
            SET status = 'idle',
                status_updated_at = NOW(),
                last_check = NOW()
            WHERE id = ANY($1)
            "#,
            &site_ids[..]
        )
        .execute(&mut *tx)
        .await?;

        tx.commit().await?;

        Ok(())
    }
}
