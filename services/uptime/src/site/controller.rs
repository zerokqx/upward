use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};

use crate::AppState;
use crate::blocked_ip::ForbiddenIpRepository;
use axum::Json;
use axum::extract::State;
use axum::http::StatusCode;
use reqwest::Url;
use tokio::net::lookup_host;

use super::domain::Site;
use super::dto::{CreateSiteDto, CreateSiteResponseDto, SiteResponseDto};

pub struct IpValidator {
    pub ip: IpAddr,
    forbidden_ip_repo: ForbiddenIpRepository,
}

#[derive(Debug)]
pub enum IpValidationError {
    IpBlocked,
    IpInvalid,
    DatabaseError(String),
}

impl IpValidator {
    pub fn new(ip: IpAddr, forbidden_ip_repo: ForbiddenIpRepository) -> Self {
        Self {
            ip,
            forbidden_ip_repo,
        }
    }

    pub async fn validate(&self) -> Result<(), IpValidationError> {
        let is_private = match self.ip {
            IpAddr::V4(ip) => self.is_forbidden_ipv4(ip),
            IpAddr::V6(ip) => self.is_forbidden_ipv6(ip),
        };
        if is_private {
            return Err(IpValidationError::IpInvalid);
        }

        let is_blocked = self
            .forbidden_ip_repo
            .is_blocked(self.ip)
            .await
            .map_err(|err| IpValidationError::DatabaseError(err.to_string()))?;

        if is_blocked {
            return Err(IpValidationError::IpBlocked);
        }

        Ok(())
    }

    pub fn is_forbidden_ipv4(&self, ip: Ipv4Addr) -> bool {
        ip.is_private()
            || ip.is_loopback()
            || ip.is_link_local()
            || ip.is_unspecified()
            || ip.is_broadcast()
            || matches!(ip.octets(), [100, 64..=127, ..])
            || matches!(ip.octets(), [192, 0, 2, ..])
            || matches!(ip.octets(), [198, 51, 100, ..])
            || matches!(ip.octets(), [203, 0, 113, ..])
            || ip.is_multicast()
    }

    pub fn is_forbidden_ipv6(&self, ip: Ipv6Addr) -> bool {
        ip.is_loopback()
            || ip.is_unspecified()
            || (ip.segments()[0] & 0xfe00) == 0xfc00
            || (ip.segments()[0] & 0xffc0) == 0xfe80
            || ip
                .to_ipv4_mapped()
                .is_some_and(|v4| self.is_forbidden_ipv4(v4))
            || ip.is_multicast()
    }
}

fn map_ip_forbidden_error_to_response(err: IpValidationError) -> (StatusCode, String) {
    match err {
        IpValidationError::IpBlocked => (StatusCode::FORBIDDEN, "IP is in forbidden list".into()),
        IpValidationError::IpInvalid => (
            StatusCode::FORBIDDEN,
            "Private, loopback or local IPs are not allowed".into(),
        ),
        IpValidationError::DatabaseError(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("Database error during IP check: {e}"),
        ),
    }
}

async fn validate_host(
    host: &str,
    port: u16,
    repo: ForbiddenIpRepository,
) -> Result<(), (StatusCode, String)> {
    // 1. Если хост уже является IP-адресом
    if let Ok(ip) = host.parse::<IpAddr>() {
        let validator = IpValidator::new(ip, repo);
        return validator
            .validate()
            .await
            .map_err(map_ip_forbidden_error_to_response);
    }

    // 2. Если хост — это доменное имя, резолвим его адреса через DNS
    let addrs = lookup_host(format!("{}:{}", host, port))
        .await
        .map_err(|e| (StatusCode::BAD_REQUEST, format!("Cannot resolve host: {e}")))?;

    for socket_addr in addrs {
        let ip = socket_addr.ip();
        let validator = IpValidator::new(ip, repo.clone());
        validator
            .validate()
            .await
            .map_err(map_ip_forbidden_error_to_response)?;
    }

    Ok(())
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
            example = json!({ "id": 1, "status": "created" })
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
    let url = Url::parse(body.site.as_ref())
        .map_err(|e| (StatusCode::BAD_REQUEST, format!("Invalid URL: {e}")))?;

    if url.scheme() != "https" && url.scheme() != "http" {
        return Err((
            StatusCode::BAD_REQUEST,
            "Only http and https schemes are allowed".into(),
        ));
    }

    let host = url
        .host_str()
        .ok_or_else(|| (StatusCode::BAD_REQUEST, "Missing host in URL".into()))?;
    let port = url.port_or_known_default().unwrap_or(80);

    validate_host(host, port, state.forbidden_ip_repo).await?;

    let site = Site::new(body.site, body.user_id);
    let site_id = state.site_repo.save_site(&site).await.map_err(|e| {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("Failed to save site: {e}"),
        )
    })?;

    Ok((
        StatusCode::CREATED,
        Json(CreateSiteResponseDto {
            id: site_id,
            status: "created",
        }),
    ))
}

/// Получить список всех отслеживаемых сайтов
///
/// Возвращает список всех зарегистрированных сайтов вместе со статусом и доп. данными последней проверки доступности.
#[tracing::instrument(skip(state))]
#[utoipa::path(
    get,
    path = "/sites",
    tag = "Sites",
    responses(
        (
            status = 200,
            description = "Список отслеживаемых сайтов с последним статусом проверки",
            body = Vec<SiteResponseDto>,
            example = json!([
                {
                    "id": 1,
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
) -> Result<Json<Vec<SiteResponseDto>>, (StatusCode, String)> {
    let sites = state
        .site_repo
        .get_all_sites()
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    Ok(Json(sites))
}
