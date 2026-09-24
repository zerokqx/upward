use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

use crate::domain::{AccessToken, RefreshToken};

/// Запрос на аутентификацию по email и паролю
#[derive(Debug, Deserialize, ToSchema)]
pub struct LoginByPasswordRequestDto {
    /// Адрес электронной почты пользователя
    #[schema(example = "user@example.com")]
    pub email: String,

    /// Пароль пользователя в открытом виде
    #[schema(example = "strongpassword123")]
    pub password: String,
}

/// Успешный ответ аутентификации с парой токенов
#[derive(Debug, Serialize, ToSchema)]
pub struct LoginByPasswordResponseDto {
    /// Короткоживущий JWT токен доступа (15 минут)
    pub access: AccessToken,

    /// Долгоживущий одноразовый Refresh токен для ротации (30 дней)
    pub refresh: RefreshToken,
}

/// Запрос на обновление пары токенов (Refresh Token Rotation)
#[derive(Debug, Deserialize, ToSchema)]
pub struct RefreshRequestDto {
    /// Текущий активный Refresh токен
    #[schema(example = "1024ad10-4b6d-490c-a55d-ed70dcbe4f84")]
    pub refresh: RefreshToken,
}

/// Запрос на регистрацию пользователя по email и паролю
#[derive(Debug, Deserialize, ToSchema)]
pub struct RegisterRequestDto {
    /// Адрес электронной почты пользователя
    #[schema(example = "newuser@example.com")]
    pub email: String,

    /// Пароль пользователя в открытом виде
    #[schema(example = "strongpassword123")]
    pub password: String,
}

/// Ответ с открытым криптографическим ключом для валидации токенов
#[derive(Debug, Serialize, ToSchema)]
pub struct PublicKeyResponseDto {
    /// Алгоритм цифровой подписи токенов
    #[schema(example = "RS256")]
    pub algorithm: String,

    /// Публичный ключ RSA в формате PEM (X.509 SubjectPublicKeyInfo)
    #[schema(example = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...\n-----END PUBLIC KEY-----")]
    pub public_key: String,
}


