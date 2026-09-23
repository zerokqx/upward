use redis::AsyncCommands;
use sqlx::PgPool;
use uuid::Uuid;

use crate::domain::{SiteId, SiteStatus, SiteUrl, UserId};

use super::domain::Site;
use super::dto::SiteResponseDto;

/// Внутренняя структура строки базы данных для выборки сайта с метаданными последнего пинга
#[derive(sqlx::FromRow)]
pub(crate) struct SiteWithLastPingDbRow {
    pub id: SiteId,
    pub user_id: UserId,
    pub url: SiteUrl,
    pub created_at: chrono::DateTime<chrono::Utc>,
    pub last_check: Option<chrono::DateTime<chrono::Utc>>,
    pub status: SiteStatus,
    pub status_updated_at: chrono::DateTime<chrono::Utc>,
    pub extra: Option<serde_json::Value>,
    pub active: bool,
}

impl From<SiteWithLastPingDbRow> for SiteResponseDto {
    fn from(row: SiteWithLastPingDbRow) -> Self {
        Self {
            id: row.id,
            user_id: row.user_id,
            url: row.url,
            created_at: row.created_at,
            last_check: row.last_check,
            status: row.status,
            status_updated_at: row.status_updated_at,
            extra: row.extra,
            active: row.active,
        }
    }
}

#[derive(Clone, Debug)]
pub struct SiteRepository {
    pool: PgPool,
}

impl SiteRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }

    pub async fn save_site(&self, site: &Site) -> Result<SiteId, sqlx::Error> {
        let res = sqlx::query!(
            r#"
        INSERT INTO sites (user_id, url, active)
        VALUES ($1, $2, $3)
        RETURNING id
        "#,
            site.user_id.0,
            site.url.0,
            site.active
        )
        .fetch_one(&self.pool)
        .await;

        match res {
            Ok(record) => Ok(SiteId(record.id)),
            Err(err) => {
                if let Some(db_err) = err.as_database_error()
                    && db_err.code() == Some("23505".into())
                {
                    println!("Попытка дублирования сайта: {}", site.url);
                }
                Err(err)
            }
        }
    }

    pub async fn get_all_sites_for_user(
        &self,
        user_id: &UserId,
    ) -> Result<Vec<SiteResponseDto>, sqlx::Error> {
        let rows = sqlx::query_as!(
            SiteWithLastPingDbRow,
            r#"
            SELECT 
                s.id as "id: SiteId", 
                s.user_id as "user_id: UserId", 
                s.url as "url: SiteUrl", 
                s.created_at, 
                s.last_check, 
                s.status as "status: SiteStatus", 
                s.status_updated_at,
                s.active,
                p.extra
            FROM sites s
            LEFT JOIN LATERAL (
                SELECT extra
                FROM site_pings
                WHERE site_id = s.id
                ORDER BY time DESC
                LIMIT 1
            ) p ON true
            WHERE s.user_id = $1
            ORDER BY s.id
            "#,
            user_id.0
        )
        .fetch_all(&self.pool)
        .await?;

        Ok(rows.into_iter().map(Into::into).collect())
    }

    pub async fn get_sites_for_ping(&self, limit: i64) -> Result<Vec<Site>, sqlx::Error> {
        let records = sqlx::query!(
            r#"
            WITH target_sites AS (
                SELECT id
                FROM sites
                WHERE active = TRUE
                  AND (
                    (status = 'idle' AND (last_check IS NULL OR last_check < NOW() - INTERVAL '60 seconds'))
                    OR (status = 'processing' AND status_updated_at < NOW() - INTERVAL '3 minutes')
                  )
                ORDER BY last_check ASC NULLS FIRST
                LIMIT $1
                FOR UPDATE SKIP LOCKED
            )
            UPDATE sites s
            SET status = 'processing',
                status_updated_at = NOW()
            FROM target_sites ts
            WHERE s.id = ts.id
            RETURNING s.id, s.url, s.user_id, s.active
            "#,
            limit
        )
        .fetch_all(&self.pool)
        .await?;

        let sites = records
            .into_iter()
            .map(|r| Site::with_id(SiteId(r.id), SiteUrl(r.url), UserId(r.user_id), r.active))
            .collect();

        Ok(sites)
    }

    pub async fn mark_sites_idle(&self, site_ids: &[SiteId]) -> Result<(), sqlx::Error> {
        if site_ids.is_empty() {
            return Ok(());
        }

        let raw_ids: Vec<uuid::Uuid> = site_ids.iter().map(|id| id.0).collect();

        sqlx::query!(
            r#"
            UPDATE sites
            SET status = 'idle',
                status_updated_at = NOW(),
                last_check = NOW()
            WHERE id = ANY($1)
            "#,
            &raw_ids[..]
        )
        .execute(&self.pool)
        .await?;

        Ok(())
    }

    pub async fn delete_site(&self, site_id: SiteId) -> Result<(), sqlx::Error> {
        sqlx::query!(
            r#"
            DELETE FROM sites
            WHERE id = $1
            "#,
            site_id.0
        )
        .execute(&self.pool)
        .await?;

        Ok(())
    }

    pub async fn get_site_by_id(&self, site_id: SiteId) -> Result<Option<Site>, sqlx::Error> {
        let record = sqlx::query!(
            r#"
            SELECT id, url, user_id, active
            FROM sites
            WHERE id = $1
            "#,
            site_id.0
        )
        .fetch_optional(&self.pool)
        .await?;

        Ok(
            record
                .map(|r| Site::with_id(SiteId(r.id), SiteUrl(r.url), UserId(r.user_id), r.active)),
        )
    }

    pub async fn activate_site(&self, site_id: SiteId) -> Result<bool, sqlx::Error> {
        let res = sqlx::query!(
            r#"
            UPDATE sites
            SET active = TRUE
            WHERE id = $1
            "#,
            site_id.0
        )
        .execute(&self.pool)
        .await?;

        Ok(res.rows_affected() > 0)
    }
}

#[derive(Clone)]
pub struct ChallengeRepository {
    redis: redis::aio::MultiplexedConnection,
}

impl ChallengeRepository {
    pub fn new(redis: redis::aio::MultiplexedConnection) -> Self {
        Self { redis }
    }

    pub async fn new_challenge(&self, site_id: SiteId) -> Result<String, redis::RedisError> {
        let mut conn = self.redis.clone();
        let token = Uuid::new_v4().to_string();
        let key = format!("challenge:{}:{}", site_id, token);
        let _: () = conn.set_ex(key, 1, 86400).await?;
        Ok(token)
    }

    pub async fn verify_challenge(
        &self,
        site_id: SiteId,
        token: &str,
    ) -> Result<bool, redis::RedisError> {
        let mut conn = self.redis.clone();
        let key = format!("challenge:{}:{}", site_id, token);
        let exists: bool = conn.exists(&key).await?;
        if exists {
            let _: () = conn.del(&key).await?;
        }
        Ok(exists)
    }
}
