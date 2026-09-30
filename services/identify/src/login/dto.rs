use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
use validator::Validate;

use crate::domain::{AccessToken, RefreshToken};

/// Запрос на аутентификацию по email и паролю
#[derive(Debug, Deserialize, ToSchema, Validate)]
pub struct LoginByPasswordRequestDto {
    /// Адрес электронной почты пользователя
    #[schema(format = Email, max_length = 320, example = "user@example.com")]
    #[validate(email, length(max = 320))]
    pub email: String,

    /// Пароль пользователя в открытом виде
    #[schema(min_length = 8, max_length = 128, example = "strongpassword123")]
    #[validate(length(min = 8, max = 128))]
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
#[derive(Debug, Deserialize, ToSchema, Validate)]
pub struct RefreshRequestDto {
    /// Текущий активный Refresh токен
    #[schema(format = Uuid, min_length = 36, max_length = 36, example = "1024ad10-4b6d-490c-a55d-ed70dcbe4f84")]
    #[validate(length(equal = 36))]
    pub refresh: RefreshToken,
}

/// Запрос на регистрацию пользователя по email и паролю
#[derive(Debug, Deserialize, ToSchema, Validate)]
pub struct RegisterRequestDto {
    /// Адрес электронной почты пользователя
    #[schema(format = Email, max_length = 320, example = "newuser@example.com")]
    #[validate(email, length(max = 320))]
    pub email: String,

    /// Пароль пользователя в открытом виде
    #[schema(min_length = 8, max_length = 128, example = "strongpassword123")]
    #[validate(length(min = 8, max = 128))]
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
