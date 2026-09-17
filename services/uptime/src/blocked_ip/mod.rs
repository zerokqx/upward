use std::net::IpAddr;

use sqlx::PgPool;

#[derive(Clone, Debug)]
pub struct ForbiddenIpRepository {
    pool: PgPool,
}
impl ForbiddenIpRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
    pub async fn is_blocked(&self, ip: IpAddr) -> Result<bool, sqlx::Error> {
        let exists: bool = sqlx::query_scalar(
            r#"SELECT EXISTS(SELECT 1 FROM forbidden_ip WHERE ip = $1) as "exists!""#,
        )
        .bind(ip.to_string())
        .fetch_one(&self.pool)
        .await?;
        Ok(exists)
    }

    pub async fn block_ip(&self, ip: IpAddr) -> Result<i64, sqlx::Error> {
        let row = sqlx::query!(
            r#"INSERT INTO forbidden_ip (ip) VALUES ($1) RETURNING id"#,
            ip.to_string()
        )
        .fetch_one(&self.pool)
        .await?;
        Ok(row.id)
    }
}
