use std::collections::HashMap;
use std::time::{Duration, Instant};

use reqwest::{StatusCode, Url};
use serde_json::Value;

use super::controller::{IpValidator, UrlValidationError};

pub const MAX_RESPONSE_BYTES: usize = 64 * 1024;

#[derive(Debug, thiserror::Error)]
pub enum ProbeError {
    #[error("URL validation failed: {0}")]
    Validation(#[from] UrlValidationError),
    #[error("Network error: {0}")]
    Network(#[from] reqwest::Error),
    #[error("Unexpected HTTP status: {0}")]
    Status(StatusCode),
    #[error("Expected application/json response")]
    ContentType,
    #[error("Response exceeds {MAX_RESPONSE_BYTES} bytes")]
    TooLarge,
    #[error("Response must be a JSON object")]
    InvalidJson,
}

pub fn endpoint_url(raw_url: &str, path: &str) -> Result<Url, UrlValidationError> {
    let mut url =
        Url::parse(raw_url).map_err(|err| UrlValidationError::InvalidUrl(err.to_string()))?;
    url.set_path(path);
    url.set_query(None);
    url.set_fragment(None);
    Ok(url)
}

pub async fn fetch_limited(
    url: &Url,
    validator: &IpValidator,
    timeout: Duration,
) -> Result<(reqwest::header::HeaderMap, Vec<u8>, Duration), ProbeError> {
    let addresses = validator.resolve_url(url.as_str()).await?;
    let host = url.host_str().ok_or(UrlValidationError::MissingHost)?;
    let client = reqwest::Client::builder()
        .no_proxy()
        .redirect(reqwest::redirect::Policy::none())
        .timeout(timeout)
        .resolve_to_addrs(host, &addresses)
        .build()?;
    let started = Instant::now();
    let mut response = client.get(url.clone()).send().await?;
    if !response.status().is_success() {
        return Err(ProbeError::Status(response.status()));
    }
    if response
        .content_length()
        .is_some_and(|len| len > MAX_RESPONSE_BYTES as u64)
    {
        return Err(ProbeError::TooLarge);
    }
    let headers = response.headers().clone();
    let mut body = Vec::new();
    while let Some(chunk) = response.chunk().await? {
        if body.len().saturating_add(chunk.len()) > MAX_RESPONSE_BYTES {
            return Err(ProbeError::TooLarge);
        }
        body.extend_from_slice(&chunk);
    }
    Ok((headers, body, started.elapsed()))
}

pub async fn probe_upward(
    raw_url: &str,
    validator: &IpValidator,
    timeout: Duration,
) -> Result<(HashMap<String, Value>, Duration), ProbeError> {
    let url = endpoint_url(raw_url, "/upward")?;
    let (headers, body, duration) = fetch_limited(&url, validator, timeout).await?;
    let is_json = headers
        .get(reqwest::header::CONTENT_TYPE)
        .and_then(|value| value.to_str().ok())
        .and_then(|value| value.split(';').next())
        .is_some_and(|value| value.trim().eq_ignore_ascii_case("application/json"));
    if !is_json {
        return Err(ProbeError::ContentType);
    }
    let value: Value = serde_json::from_slice(&body).map_err(|_| ProbeError::InvalidJson)?;
    let object = value.as_object().ok_or(ProbeError::InvalidJson)?;
    Ok((object.clone().into_iter().collect(), duration))
}
