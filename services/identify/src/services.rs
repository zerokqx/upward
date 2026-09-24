use std::sync::Arc;
use chrono::{Duration, Utc};
use jsonwebtoken::{decode, encode, Algorithm, DecodingKey, EncodingKey, Header, Validation};
use redis::AsyncCommands;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::domain::{AccessToken, RefreshToken};

/// Полезная нагрузка токена (JWT Claims)
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Claims {
    pub sub: Uuid,
    pub email: String,
    pub exp: usize,
    pub iat: usize,
}

/// Сервис для работы с JWT и токенами аутентификации (асимметричная цифровая подпись RS256)
#[derive(Clone)]
pub struct JwtService {
    encoding_key: Arc<EncodingKey>,
    decoding_key: Arc<DecodingKey>,
    public_key_pem: String,
    access_token_ttl_seconds: i64,
    refresh_token_ttl_seconds: u64,
}

impl std::fmt::Debug for JwtService {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("JwtService")
            .field("access_token_ttl_seconds", &self.access_token_ttl_seconds)
            .field("refresh_token_ttl_seconds", &self.refresh_token_ttl_seconds)
            .finish()
    }
}

impl JwtService {
    pub fn new(private_key_pem: &str, public_key_pem: &str) -> Result<Self, jsonwebtoken::errors::Error> {
        let encoding_key = EncodingKey::from_rsa_pem(private_key_pem.as_bytes())?;
        let decoding_key = DecodingKey::from_rsa_pem(public_key_pem.as_bytes())?;

        Ok(Self {
            encoding_key: Arc::new(encoding_key),
            decoding_key: Arc::new(decoding_key),
            public_key_pem: public_key_pem.trim().to_string(),
            access_token_ttl_seconds: 15 * 60, // 15 минут
            refresh_token_ttl_seconds: 30 * 24 * 60 * 60, // 30 дней
        })
    }

    /// Открытый криптографический ключ (RSA PEM)
    pub fn public_key_pem(&self) -> &str {
        &self.public_key_pem
    }

    /// Генерация access токена (JWT RS256)
    pub fn generate_access_token(
        &self,
        user_id: Uuid,
        email: &str,
    ) -> Result<AccessToken, jsonwebtoken::errors::Error> {
        let now = Utc::now();
        let exp = now + Duration::seconds(self.access_token_ttl_seconds);

        let claims = Claims {
            sub: user_id,
            email: email.to_string(),
            iat: now.timestamp() as usize,
            exp: exp.timestamp() as usize,
        };

        let header = Header::new(Algorithm::RS256);
        let token = encode(&header, &claims, &self.encoding_key)?;

        Ok(AccessToken(token))
    }

    /// Генерация пары (access_token, refresh_token) с сохранением refresh-токена в Redis
    pub async fn generate_token_pair(
        &self,
        user_id: Uuid,
        email: &str,
        redis: &mut redis::aio::MultiplexedConnection,
    ) -> Result<(AccessToken, RefreshToken), Box<dyn std::error::Error + Send + Sync>> {
        let access = self.generate_access_token(user_id, email)?;
        let refresh_id = Uuid::new_v4().to_string();

        let redis_key = format!("refresh:{}", refresh_id);
        redis
            .set_ex::<_, _, ()>(redis_key, user_id.to_string(), self.refresh_token_ttl_seconds)
            .await?;

        Ok((access, RefreshToken(refresh_id)))
    }

    /// Проверка и декодирование access токена с использованием публичного ключа
    pub fn verify_access_token(
        &self,
        token: &str,
    ) -> Result<Claims, jsonwebtoken::errors::Error> {
        let validation = Validation::new(Algorithm::RS256);
        let token_data = decode::<Claims>(
            token,
            &self.decoding_key,
            &validation,
        )?;
        Ok(token_data.claims)
    }

    /// Проверка и обновление пары токенов (Refresh Token Rotation)
    pub async fn refresh_token_pair(
        &self,
        old_refresh: &RefreshToken,
        user_repo: &crate::login::UserRepository,
        redis: &mut redis::aio::MultiplexedConnection,
    ) -> Result<(AccessToken, RefreshToken), RefreshError> {
        let redis_key = format!("refresh:{}", old_refresh.as_str());

        // 1. Проверяем токен в Redis
        let user_id_str: Option<String> = redis
            .get(&redis_key)
            .await
            .map_err(|e| RefreshError::RedisError(e.to_string()))?;

        let user_id_str = user_id_str.ok_or(RefreshError::InvalidOrExpiredToken)?;
        let user_id: Uuid = user_id_str
            .parse()
            .map_err(|_| RefreshError::InvalidOrExpiredToken)?;

        // 2. Одноразовость: удаляем старый refresh токен
        let _: () = redis
            .del(&redis_key)
            .await
            .map_err(|e| RefreshError::RedisError(e.to_string()))?;

        // 3. Проверяем, существует ли пользователь в БД
        let user = user_repo
            .find_by_id(user_id)
            .await
            .map_err(|e| RefreshError::DatabaseError(e.to_string()))?
            .ok_or(RefreshError::UserNotFound)?;

        // 4. Выпускаем новую пару (access + refresh) и сохраняем новый refresh в Redis
        let (new_access, new_refresh) = self
            .generate_token_pair(user.id, &user.email, redis)
            .await
            .map_err(|e| RefreshError::InternalError(e.to_string()))?;

        Ok((new_access, new_refresh))
    }
}

/// Ошибки при обновлении токена
#[derive(Debug, thiserror::Error)]
pub enum RefreshError {
    #[error("Invalid or expired refresh token")]
    InvalidOrExpiredToken,
    #[error("User not found")]
    UserNotFound,
    #[error("Redis error: {0}")]
    RedisError(String),
    #[error("Database error: {0}")]
    DatabaseError(String),
    #[error("Internal error: {0}")]
    InternalError(String),
}

#[cfg(test)]
mod tests {
    use super::*;
    use argon2::{
        password_hash::{PasswordHash, PasswordVerifier},
        Argon2,
    };

    #[test]
    fn test_jwt_and_argon2_verify() {
        use argon2::password_hash::PasswordHasher;

        // Генерируем реальный хеш для "password"
        let hash = Argon2::default()
            .hash_password_with_salt(b"password", b"random_salt_1234")
            .unwrap();
        let hash_str = hash.to_string();
        println!("HASH_OUTPUT: {}", hash_str);

        let parsed_hash = PasswordHash::new(&hash_str).unwrap();
        assert!(Argon2::default().verify_password(b"password", &parsed_hash).is_ok());
        assert!(Argon2::default().verify_password(b"wrongpass", &parsed_hash).is_err());

        // Проверяем JWT
        let jwt_service = JwtService::new("test_secret".to_string());
        let user_id = Uuid::new_v4();
        let token = jwt_service
            .generate_access_token(user_id, "test@example.com")
            .unwrap();
        let claims = jwt_service.verify_access_token(token.as_str()).unwrap();
        assert_eq!(claims.sub, user_id);
        assert_eq!(claims.email, "test@example.com");
    }
}
