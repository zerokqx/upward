mod blocked_ip;
mod domain;
mod openapi;
mod ping;
mod site;

use axum::Json;
use axum::routing::post;
use axum::{Router, http::StatusCode, routing::get};
use dotenvy::dotenv;
use reqwest::redirect;
use serde::Serialize;
use sqlx::PgPool;
use sqlx::postgres::PgPoolOptions;
use std::env;
use std::time::Duration;
use tokio::task::JoinHandle;
use tokio::time::interval;
use tracing::{Level, debug};
use tracing_subscriber::FmtSubscriber;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

use futures::stream::{self, StreamExt};

use self::blocked_ip::ForbiddenIpRepository;
use self::domain::SiteId;
use self::openapi::ApiDoc;
use self::ping::domain::PingRecord;
use self::ping::infrastructure::HttpPinger;
use self::ping::repository::PingRepository;
use self::site::controller::{create_site, get_all_sites};
use self::site::repository::SiteRepository;

#[derive(Clone, Debug)]
pub struct AppState {
    pub pool: PgPool,
    pub site_repo: SiteRepository,
    pub ping_repo: PingRepository,
    pub forbidden_ip_repo: ForbiddenIpRepository,
}

async fn check_all_sites(pool: &PgPool) -> JoinHandle<()> {
    let pool = pool.clone();
    tokio::spawn(async move {
        let mut ticker = interval(Duration::from_secs(10));
        let client = reqwest::ClientBuilder::new()
            .user_agent("UptimeMonitor/1.0")
            .redirect(redirect::Policy::limited(5))
            .timeout(Duration::from_secs(10))
            .build()
            .unwrap();
        let pinger = HttpPinger::new(&client);
        let site_repo = SiteRepository::new(pool.clone());
        let ping_repo = PingRepository::new(pool);
        loop {
            ticker.tick().await;
            match site_repo.get_sites_for_ping(500).await {
                Ok(sites) => {
                    if sites.is_empty() {
                        continue;
                    }
                    println!("Fetched {} sites for ping...", sites.len());

                    let results: Vec<PingRecord> = stream::iter(sites)
                        .map(|site| {
                            let pinger = pinger.clone();
                            async move {
                                let site_id = site.id.expect("site id required");
                                match pinger.ping(site.url.as_ref()).await {
                                    Ok(resp) => PingRecord {
                                        site_id,
                                        duration_ms: resp.ping_duration.as_secs_f64() * 1000.0,
                                        extra: serde_json::to_value(resp.extra).unwrap_or_default(),
                                    },
                                    Err(err) => PingRecord {
                                        site_id,
                                        duration_ms: 0.0,
                                        extra: serde_json::json!({ "error": err.to_string() }),
                                    },
                                }
                            }
                        })
                        .buffer_unordered(25)
                        .collect()
                        .await;

                    println!("Pings completed, saving {} results...", results.len());
                    if let Err(err) = ping_repo.save_pings_batch(&results).await {
                        eprintln!("Error saving batch pings: {}", err);
                    } else {
                        println!("Successfully saved batch of {} pings", results.len());
                    }

                    let site_ids: Vec<SiteId> = results.iter().map(|r| r.site_id).collect();
                    if let Err(err) = site_repo.mark_sites_idle(&site_ids).await {
                        eprintln!("Error updating sites status: {}", err);
                    }
                }
                Err(err) => {
                    eprintln!("Error fetching sites for ping: {}", err);
                }
            }
        }
    })
}

/// Ответ эндпоинта проверки работоспособности сервиса
#[derive(Serialize, utoipa::ToSchema)]
pub struct HealthResponseDto {
    /// Статус состояния сервиса
    #[schema(example = "ok")]
    pub status: &'static str,

    /// Пояснительное сообщение
    #[schema(example = "Uptime monitoring service is running")]
    pub message: &'static str,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenv().expect(".env file not found");
    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::DEBUG)
        .finish();
    tracing::subscriber::set_global_default(subscriber).expect("setting default subscriber failed");
    let port = env::var("PORT").unwrap_or_else(|_| "3000".to_string());
    let host = env::var("HOST").unwrap_or_else(|_| "127.0.0.1".to_string());
    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .unwrap();

    let app = Router::new()
        .merge(SwaggerUi::new("/docs").url("/docs/docs.json", ApiDoc::openapi()))
        .route("/health", get(health_check))
        .route("/sites", get(get_all_sites))
        .route("/sites", post(create_site))
        .with_state(AppState {
            pool: pool.clone(),
            forbidden_ip_repo: blocked_ip::ForbiddenIpRepository::new(pool.clone()),
            site_repo: SiteRepository::new(pool.clone()),
            ping_repo: PingRepository::new(pool.clone()),
        });
    let listner = tokio::net::TcpListener::bind(format!("{}:{}", host, port)).await?;
    check_all_sites(&pool).await;
    debug!("Запускаем на порту {}", &port);
    axum::serve(listner, app).await?;
    Ok(())
}

/// Проверка работоспособности сервиса (Health Check)
///
/// Возвращает текущее состояние доступности микросервиса.
/// Используется оркестратором (Docker, Kubernetes) для liveness и readiness проб.
#[tracing::instrument]
#[utoipa::path(
    get,
    path = "/health",
    tag = "Health",
    responses(
        (
            status = 200,
            description = "Сервис успешно запущен и обрабатывает запросы",
            body = HealthResponseDto,
            example = json!({
                "status": "ok",
                "message": "Uptime monitoring service is running"
            })
        )
    )
)]
pub async fn health_check() -> (StatusCode, Json<HealthResponseDto>) {
    let response = HealthResponseDto {
        status: "ok",
        message: "Uptime monitoring service is running",
    };
    (StatusCode::OK, Json(response))
}
