use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};

use crate::AppState;
use crate::blocked_ip::ForbiddenIpRepository;
use axum::Json;
use axum::extract::State;
use axum::http::StatusCode;
use reqwest::Url;
use serde::Deserialize;
use tokio::net::lookup_host;

use super::domain::{Site, UserId};

#[derive(Deserialize)]
pub struct CreateSiteDto {
    pub user_id: UserId,
    pub site: String,
}

pub struct IpValidation {
    pub ip: IpAddr,
    forbidden_ip_repo: ForbiddenIpRepository,
}

#[derive(Debug)]
pub enum IsForbiddenIpError {
    IpBlocked,
    IpInvalid,
    DatabaseError(String),
}

impl IpValidation {
    pub fn new(ip: IpAddr, forbidden_ip_repo: ForbiddenIpRepository) -> Self {
        Self {
            ip,
            forbidden_ip_repo,
        }
    }

    pub async fn is_forbidden_ip(&self) -> Result<(), IsForbiddenIpError> {
        let is_private = match self.ip {
            IpAddr::V4(ip) => self.is_forbidden_ipv4(ip),
            IpAddr::V6(ip) => self.is_forbidden_ipv6(ip),
        };
        if is_private {
            return Err(IsForbiddenIpError::IpInvalid);
        }

        let is_blocked = self
            .forbidden_ip_repo
            .is_blocked(self.ip)
            .await
            .map_err(|err| IsForbiddenIpError::DatabaseError(err.to_string()))?;

        if is_blocked {
            return Err(IsForbiddenIpError::IpBlocked);
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

fn map_ip_forbidden_error_to_response(err: IsForbiddenIpError) -> (StatusCode, String) {
    match err {
        IsForbiddenIpError::IpBlocked => (StatusCode::FORBIDDEN, "IP is in forbidden list".into()),
        IsForbiddenIpError::IpInvalid => (
            StatusCode::FORBIDDEN,
            "Private, loopback or local IPs are not allowed".into(),
        ),
        IsForbiddenIpError::DatabaseError(e) => (
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
        let validator = IpValidation::new(ip, repo);
        return validator
            .is_forbidden_ip()
            .await
            .map_err(map_ip_forbidden_error_to_response);
    }

    // 2. Если хост — это доменное имя, резолвим его адреса через DNS
    let addrs = lookup_host(format!("{}:{}", host, port))
        .await
        .map_err(|e| (StatusCode::BAD_REQUEST, format!("Cannot resolve host: {e}")))?;

    for socket_addr in addrs {
        let ip = socket_addr.ip();
        let validator = IpValidation::new(ip, repo.clone());
        validator
            .is_forbidden_ip()
            .await
            .map_err(map_ip_forbidden_error_to_response)?;
    }

    Ok(())
}

pub async fn create_site(
    State(state): State<AppState>,
    Json(body): Json<CreateSiteDto>,
) -> Result<(StatusCode, Json<serde_json::Value>), (StatusCode, String)> {
    let url = Url::parse(&body.site)
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
    let site_id = state
        .site_repo
        .save_site(&site)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("Failed to save site: {e}")))?;

    Ok((
        StatusCode::CREATED,
        Json(serde_json::json!({ "id": site_id, "status": "created" })),
    ))
}
