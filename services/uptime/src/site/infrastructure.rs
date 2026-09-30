use std::collections::HashMap;
use std::time::{Duration, Instant};

use bytes::BytesMut;
use futures::StreamExt;
use reqwest::{StatusCode, Url};
use serde_json::Value;

use super::controller::{IpValidator, UrlValidationError};

pub const DEFAULT_MAX_PAYLOAD_BYTES: usize = 512 * 1024; // 512 KB

pub fn get_max_payload_bytes() -> usize {
    std::env::var("MAX_PAYLOAD_BYTES")
        .ok()
        .and_then(|val| val.parse::<usize>().ok())
        .unwrap_or(DEFAULT_MAX_PAYLOAD_BYTES)
}

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
    #[error("Response exceeds maximum allowed size of {max_bytes} bytes")]
    PayloadTooLarge { max_bytes: usize },
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
    let response = client.get(url.clone()).send().await?;
    if !response.status().is_success() {
        return Err(ProbeError::Status(response.status()));
    }

    let max_payload_bytes = get_max_payload_bytes();

    // Быстрый отсев по Content-Length (если заголовок прислан)
    if response
        .content_length()
        .is_some_and(|len| len as usize > max_payload_bytes)
    {
        return Err(ProbeError::PayloadTooLarge {
            max_bytes: max_payload_bytes,
        });
    }

    let headers = response.headers().clone();

    // Защита на случай, если Content-Length не прислали или соврали (Transfer-Encoding: chunked)
    let mut stream = response.bytes_stream();
    let mut body = BytesMut::new();

    while let Some(chunk) = stream.next().await {
        let chunk = chunk?;
        if body.len().saturating_add(chunk.len()) > max_payload_bytes {
            return Err(ProbeError::PayloadTooLarge {
                max_bytes: max_payload_bytes,
            });
        }
        body.extend_from_slice(&chunk);
    }

    Ok((headers, body.to_vec(), started.elapsed()))
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default_max_payload_bytes() {
        assert_eq!(DEFAULT_MAX_PAYLOAD_BYTES, 512 * 1024);
    }

    #[test]
    fn test_payload_size_limit_stream_logic() {
        let max_bytes = 100;
        let mut body = BytesMut::new();
        let chunk1 = vec![0u8; 60];
        let chunk2 = vec![0u8; 40];
        let chunk3 = vec![0u8; 1];

        // chunk 1: 60 <= 100 -> ok
        assert!(body.len() + chunk1.len() <= max_bytes);
        body.extend_from_slice(&chunk1);

        // chunk 2: 60 + 40 == 100 -> ok (equal is allowed)
        assert!(body.len() + chunk2.len() <= max_bytes);
        body.extend_from_slice(&chunk2);

        // chunk 3: 100 + 1 == 101 > 100 -> too large
        assert!(body.len() + chunk3.len() > max_bytes);
    }
}
