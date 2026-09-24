use chrono::{DateTime, Utc};
use sqlx::PgPool;
use uuid::Uuid;

/// Модель пользователя из таблицы `users`
#[derive(Debug, Clone)]
pub struct UserRecord {
    pub id: Uuid,
    pub email: String,
    /// Хеш пароля (Argon2). Может быть `None` для пользователей, вошедших через OAuth (Google)
    pub password_hash: Option<String>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

/// Репозиторий для работы с пользователями при аутентификации
#[derive(Clone, Debug)]
pub struct UserRepository {
    pool: PgPool,
}

impl UserRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }

    /// Поиск пользователя по email (case-insensitive) для входа по паролю
    pub async fn find_by_email(&self, email: &str) -> Result<Option<UserRecord>, sqlx::Error> {
        let user = sqlx::query_as!(
            UserRecord,
            r#"
            SELECT id, email, password_hash, created_at, updated_at
            FROM users
            WHERE LOWER(email) = LOWER($1)
            "#,
            email
        )
        .fetch_optional(&self.pool)
        .await?;

        Ok(user)
    }

    /// Поиск пользователя по первичному ключу (UUID)
    pub async fn find_by_id(&self, id: Uuid) -> Result<Option<UserRecord>, sqlx::Error> {
        let user = sqlx::query_as!(
            UserRecord,
            r#"
            SELECT id, email, password_hash, created_at, updated_at
            FROM users
            WHERE id = $1
            "#,
            id
        )
        .fetch_optional(&self.pool)
        .await?;

        Ok(user)
    }

    /// Создание нового пользователя с паролем (хешем Argon2)
    pub async fn create_user(&self, email: &str, password_hash: &str) -> Result<UserRecord, sqlx::Error> {
        let user = sqlx::query_as!(
            UserRecord,
            r#"
            INSERT INTO users (email, password_hash)
            VALUES ($1, $2)
            RETURNING id, email, password_hash, created_at, updated_at
            "#,
            email,
            password_hash
        )
        .fetch_one(&self.pool)
        .await?;

        Ok(user)
    }
}
