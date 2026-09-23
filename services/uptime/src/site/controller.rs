use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};

use crate::AppState;
use crate::blocked_ip::ForbiddenIpRepository;
use crate::domain::{SiteId, UserId};
use axum::Json;
use axum::extract::{Path, State};
use axum::http::StatusCode;
use axum::routing::{Router, get, post};
use reqwest::Url;
use tokio::net::lookup_host;

use super::domain::Site;
use super::dto::{CreateSiteDto, CreateSiteResponseDto, SiteResponseDto, VerifySiteResponseDto};

#[derive(Clone)]
pub struct IpValidator {
    forbidden_ip_repo: ForbiddenIpRepository,
    allow_private_ips: bool,
}

#[derive(Debug, thiserror::Error, Eq, PartialEq)]
pub enum IpValidationError {
    #[error("IP is in forbidden list")]
    IpBlocked,
    #[error("Private, loopback or local IPs are not allowed")]
    IpInvalid,
    #[error("Database error during IP check: {0}")]
    DatabaseError(String),
}

#[derive(Debug, thiserror::Error, Eq, PartialEq)]
pub enum UrlValidationError {
    #[error("Invalid URL: {0}")]
    InvalidUrl(String),
    #[error("Only http and https schemes are allowed")]
    UnsupportedScheme,
    #[error("Missing host in URL")]
    MissingHost,
    #[error("Cannot resolve host: {0}")]
    DnsError(String),
    #[error("IP is in forbidden list")]
    IpBlocked,
    #[error("Private, loopback or local IPs are not allowed")]
    IpInvalid,
    #[error("Database error during IP check: {0}")]
    DatabaseError(String),
}

impl From<IpValidationError> for UrlValidationError {
    fn from(err: IpValidationError) -> Self {
        match err {
            IpValidationError::IpBlocked => Self::IpBlocked,
            IpValidationError::IpInvalid => Self::IpInvalid,
            IpValidationError::DatabaseError(e) => Self::DatabaseError(e),
        }
    }
}

impl IpValidator {
    pub fn new(forbidden_ip_repo: ForbiddenIpRepository) -> Self {
        let allow_private_ips = std::env::var("ALLOW_PRIVATE_IPS")
            .map(|v| v.eq_ignore_ascii_case("true") || v == "1")
            .unwrap_or(false);

        Self {
            forbidden_ip_repo,
            allow_private_ips,
        }
    }

    #[allow(dead_code)]
    pub fn with_allow_private_ips(mut self, allow: bool) -> Self {
        self.allow_private_ips = allow;
        self
    }

    pub async fn validate(&self, ip: IpAddr) -> Result<(), IpValidationError> {
        let is_private = match ip {
            IpAddr::V4(v4) => Self::is_forbidden_ipv4(v4),
            IpAddr::V6(v6) => Self::is_forbidden_ipv6(v6),
        };
        if is_private && !self.allow_private_ips {
            return Err(IpValidationError::IpInvalid);
        }

        let is_blocked = self
            .forbidden_ip_repo
            .is_blocked(ip)
            .await
            .map_err(|err| IpValidationError::DatabaseError(err.to_string()))?;

        if is_blocked {
            return Err(IpValidationError::IpBlocked);
        }

        Ok(())
    }

    pub async fn validate_url(&self, raw_url: &str) -> Result<(), UrlValidationError> {
        let url = Url::parse(raw_url).map_err(|e| UrlValidationError::InvalidUrl(e.to_string()))?;

        if url.scheme() != "https" && url.scheme() != "http" {
            return Err(UrlValidationError::UnsupportedScheme);
        }

        let host = url.host_str().ok_or(UrlValidationError::MissingHost)?;
        let port = url.port_or_known_default().unwrap_or(80);

        // 1. Если хост уже является IP-адресом
        if let Ok(ip) = host.parse::<IpAddr>() {
            self.validate(ip).await?;
            return Ok(());
        }

        // 2. Если хост — домен, резолвим все целевые адреса через DNS
        let addrs = lookup_host(format!("{}:{}", host, port))
            .await
            .map_err(|e| UrlValidationError::DnsError(e.to_string()))?;

        for socket_addr in addrs {
            self.validate(socket_addr.ip()).await?;
        }

        Ok(())
    }

    pub fn is_forbidden_ipv4(ip: Ipv4Addr) -> bool {
        ip.is_private()
            || ip.is_loopback()
            || ip.is_link_local()
            || ip.is_unspecified()
            || ip.is_broadcast()
            || matches!(ip.octets(), [100, 64..=127, ..])
            || matches!(ip.octets(), [192, 0, 2, ..])
            || matches!(ip.octets(), [198, 51, 100, ..])
            || matches!(ip.octets(), [203, 0, 113, ..])
            || matches!(ip.octets()[0], 0)
            || ip.is_multicast()
    }

    pub fn is_forbidden_ipv6(ip: Ipv6Addr) -> bool {
        ip.is_loopback()
            || ip.is_unspecified()
            || (ip.segments()[0] & 0xfe00) == 0xfc00
            || (ip.segments()[0] & 0xffc0) == 0xfe80
            || ip.to_ipv4_mapped().is_some_and(Self::is_forbidden_ipv4)
            || ip.is_multicast()
    }
}

fn map_url_validation_error_to_response(err: UrlValidationError) -> (StatusCode, String) {
    match err {
        UrlValidationError::InvalidUrl(e) => (StatusCode::BAD_REQUEST, format!("Invalid URL: {e}")),
        UrlValidationError::UnsupportedScheme => (
            StatusCode::BAD_REQUEST,
            "Only http and https schemes are allowed".into(),
        ),
        UrlValidationError::MissingHost => (StatusCode::BAD_REQUEST, "Missing host in URL".into()),
        UrlValidationError::DnsError(e) => {
            (StatusCode::BAD_REQUEST, format!("Cannot resolve host: {e}"))
        }
        UrlValidationError::IpBlocked => (StatusCode::FORBIDDEN, "IP is in forbidden list".into()),
        UrlValidationError::IpInvalid => (
            StatusCode::FORBIDDEN,
            "Private, loopback or local IPs are not allowed".into(),
        ),
        UrlValidationError::DatabaseError(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("Database error during IP check: {e}"),
        ),
    }
}

/// Добавить новый сайт в мониторинг
///
/// Регистрирует URL сайта для периодической проверки доступности.
/// Выполняет DNS-резолвинг и проверяет, что целевой IP-адрес не является приватным,
/// локальным (loopback) или заблокированным в таблице `forbidden_ip`.
#[tracing::instrument(skip(state))]
#[utoipa::path(
    post,
    path = "/sites",
    tag = "Sites",
    request_body(
        content = CreateSiteDto,
        description = "Данные для регистрации сайта в системе мониторинга",
        example = json!({
            "user_id": "usr_01J8ABCDEF1234567890",
            "site": "https://example.com"
        })
    ),
    responses(
        (
            status = 201,
            description = "Сайт успешно добавлен в систему мониторинга",
            body = CreateSiteResponseDto,
            example = json!({
                "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "status": "pending_verification",
                "challenge_token": "b428d082-356a-4b92-808c-901a1e582845",
                "challenge_path": "/.well-known/upward"
            })
        ),
        (
            status = 400,
            description = "Некорректный запрос: невалидный URL, неподдерживаемая схема или ошибка DNS-резолвинга",
            body = String,
            example = json!("Only http and https schemes are allowed")
        ),
        (
            status = 403,
            description = "Запрещено: целевой IP является приватным, локальным или заблокирован",
            body = String,
            example = json!("Private, loopback or local IPs are not allowed")
        ),
        (
            status = 500,
            description = "Внутренняя ошибка сервера или базы данных",
            body = String,
            example = json!("Failed to save site: database error")
        )
    )
)]
pub async fn create_site(
    State(state): State<AppState>,
    Json(body): Json<CreateSiteDto>,
) -> Result<(StatusCode, Json<CreateSiteResponseDto>), (StatusCode, String)> {
    let validator = IpValidator::new(state.forbidden_ip_repo);
    validator
        .validate_url(body.site.as_ref())
        .await
        .map_err(map_url_validation_error_to_response)?;

    let site = Site::new(body.site, body.user_id);
    let site_id = state.site_repo.save_site(&site).await.map_err(|e| {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("Failed to save site: {e}"),
        )
    })?;

    let challenge_token = match state.challenge_repo.new_challenge(site_id).await {
        Ok(token) => token,
        Err(err) => {
            let _ = state.site_repo.delete_site(site_id).await;
            return Err((
                StatusCode::INTERNAL_SERVER_ERROR,
                format!("Failed to generate challenge token: {err}"),
            ));
        }
    };

    Ok((
        StatusCode::CREATED,
        Json(CreateSiteResponseDto {
            id: site_id,
            status: "pending_verification",
            challenge_token,
            challenge_path: "/.well-known/upward",
        }),
    ))
}

/// Получить список отслеживаемых сайтов пользователя
///
/// Возвращает список всех зарегистрированных сайтов конкретного пользователя вместе со статусом и доп. данными последней проверки доступности.
#[tracing::instrument(skip(state))]
#[utoipa::path(
    get,
    path = "/sites/{user_id}",
    tag = "Sites",
    params(
        ("user_id" = String, Path, description = "Идентификатор пользователя-владельца сайтов", example = "usr_01J8ABCDEF1234567890")
    ),
    responses(
        (
            status = 200,
            description = "Список отслеживаемых сайтов с последним статусом проверки",
            body = Vec<SiteResponseDto>,
            example = json!([
                {
                    "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                    "user_id": "usr_01J8ABCDEF1234567890",
                    "url": "https://example.com",
                    "created_at": "2026-09-15T12:00:00Z",
                    "last_check": "2026-09-15T12:05:00Z",
                    "status": "idle",
                    "status_updated_at": "2026-09-15T12:05:00Z",
                    "extra": {
                        "status_code": 200,
                        "duration_ms": 142.5
                    }
                }
            ])
        ),
        (
            status = 500,
            description = "Внутренняя ошибка сервера при чтении из базы данных",
            body = String,
            example = json!("Database query error")
        )
    )
)]
pub async fn get_all_sites(
    State(state): State<AppState>,
    Path(user_id): Path<UserId>,
) -> Result<Json<Vec<SiteResponseDto>>, (StatusCode, String)> {
    let sites = state
        .site_repo
        .get_all_sites_for_user(&user_id)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    Ok(Json(sites))
}

/// Подтвердить владение сайтом через HTTP-01 Challenge
///
/// Обращается по адресу {site.url}/.well-known/upward и сравнивает полученный токен
/// с ожидаемым токеном из Redis. При совпадении активирует сайт (active = true).
#[tracing::instrument(skip(state))]
#[utoipa::path(
    post,
    path = "/sites/{site_id}/verify",
    tag = "Sites",
    params(
        ("site_id" = String, Path, description = "Идентификатор подтверждаемого сайта", example = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11")
    ),
    responses(
        (
            status = 200,
            description = "Владение сайтом успешно подтверждено, сайт активирован",
            body = VerifySiteResponseDto,
            example = json!({ "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "status": "verified" })
        ),
        (
            status = 400,
            description = "Некорректный запрос: токен не совпадает, челендж протух или некорректный ответ сайта",
            body = String,
            example = json!("Challenge token mismatch or expired")
        ),
        (
            status = 404,
            description = "Сайт не найден",
            body = String,
            example = json!("Site not found")
        ),
        (
            status = 502,
            description = "Ошибка связи с целевым сайтом",
            body = String,
            example = json!("Failed to reach challenge URL: connection refused")
        )
    )
)]
pub async fn verify_site(
    State(state): State<AppState>,
    Path(site_id): Path<SiteId>,
) -> Result<Json<VerifySiteResponseDto>, (StatusCode, String)> {
    let site = state
        .site_repo
        .get_site_by_id(site_id)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?
        .ok_or_else(|| (StatusCode::NOT_FOUND, "Site not found".into()))?;

    if site.active {
        return Ok(Json(VerifySiteResponseDto {
            id: site_id,
            status: "already_verified",
        }));
    }

    let mut verify_url = Url::parse(site.url.as_ref())
        .map_err(|e| (StatusCode::BAD_REQUEST, format!("Invalid site URL: {e}")))?;
    verify_url.set_path("/.well-known/upward");

    // Защита от SSRF и DNS Rebinding перед запросом
    let validator = IpValidator::new(state.forbidden_ip_repo);
    validator
        .validate_url(verify_url.as_str())
        .await
        .map_err(map_url_validation_error_to_response)?;

    let client = reqwest::Client::builder()
        .timeout(std::time::Duration::from_secs(5))
        .redirect(reqwest::redirect::Policy::none())
        .build()
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    let resp = client.get(verify_url.as_str()).send().await.map_err(|e| {
        (
            StatusCode::BAD_GATEWAY,
            format!("Failed to reach challenge URL: {e}"),
        )
    })?;

    if !resp.status().is_success() {
        return Err((
            StatusCode::BAD_REQUEST,
            format!("Challenge URL returned HTTP status {}", resp.status()),
        ));
    }

    let returned_token = resp.text().await.map_err(|e| {
        (
            StatusCode::BAD_GATEWAY,
            format!("Failed to read response from challenge URL: {e}"),
        )
    })?;

    let is_valid = state
        .challenge_repo
        .verify_challenge(site_id, returned_token.trim())
        .await
        .map_err(|e| {
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                format!("Redis verification error: {e}"),
            )
        })?;

    if !is_valid {
        return Err((
            StatusCode::BAD_REQUEST,
            "Challenge token mismatch or expired".into(),
        ));
    }

    state
        .site_repo
        .activate_site(site_id)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    Ok(Json(VerifySiteResponseDto {
        id: site_id,
        status: "verified",
    }))
}

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/sites/{user_id}", get(get_all_sites))
        .route("/sites", post(create_site))
        .route("/sites/{site_id}/verify", post(verify_site))
}
#[cfg(test)]
mod tests {
    use super::*;
    use sqlx::PgPool;

    #[test]
    fn test_forbidden_ipv4_pure() {
        assert!(IpValidator::is_forbidden_ipv4("127.0.0.1".parse().unwrap()));
        assert!(IpValidator::is_forbidden_ipv4(
            "192.168.1.1".parse().unwrap()
        ));
        assert!(IpValidator::is_forbidden_ipv4("10.0.0.1".parse().unwrap()));
        assert!(IpValidator::is_forbidden_ipv4("0.0.0.1".parse().unwrap()));
        assert!(IpValidator::is_forbidden_ipv4(
            "0.255.255.254".parse().unwrap()
        ));
        assert!(!IpValidator::is_forbidden_ipv4("8.8.8.8".parse().unwrap()));
    }

    #[sqlx::test(migrations = "./migrations")]
    async fn test_ip_validation(pool: PgPool) {
        let repo = ForbiddenIpRepository::new(pool);
        let blocked_ip: IpAddr = "93.184.216.34".parse().unwrap();
        repo.block_ip(blocked_ip).await.unwrap();

        let validator = IpValidator::new(repo.clone()).with_allow_private_ips(false);

        // 1. Локальный IP -> IpInvalid
        assert_eq!(
            validator.validate("127.0.0.1".parse().unwrap()).await,
            Err(IpValidationError::IpInvalid)
        );

        // 2. Заблокированный в БД IP -> IpBlocked
        assert_eq!(
            validator.validate(blocked_ip).await,
            Err(IpValidationError::IpBlocked)
        );

        // 3. Нормальный публичный IP -> Ok
        assert_eq!(validator.validate("8.8.8.8".parse().unwrap()).await, Ok(()));

        // 4. URL с локальным IP -> IpInvalid
        assert_eq!(
            validator.validate_url("http://127.0.0.1:8080/test").await,
            Err(UrlValidationError::IpInvalid)
        );

        // 5. Неподдерживаемая схема -> UnsupportedScheme
        assert_eq!(
            validator.validate_url("ftp://example.com").await,
            Err(UrlValidationError::UnsupportedScheme)
        );

        // 6. Режим разработки с allow_private_ips -> Ok
        let dev_validator = IpValidator::new(repo).with_allow_private_ips(true);
        assert_eq!(
            dev_validator.validate("127.0.0.1".parse().unwrap()).await,
            Ok(())
        );
        assert_eq!(
            dev_validator
                .validate_url("http://127.0.0.1:8080/test")
                .await,
            Ok(())
        );
    }
}
