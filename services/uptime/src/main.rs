mod blocked_ip;
mod site;
use std::env;
use std::time::Duration;

use axum::Json;
use axum::extract::State;
use axum::routing::post;
use axum::{Router, http::StatusCode, routing::get};
use dotenvy::dotenv;
use reqwest::redirect;
use serde::Serialize;
use sqlx::PgPool;
use sqlx::postgres::PgPoolOptions;
use tokio::task::JoinHandle;
use tokio::time::interval;

use futures::stream::{self, StreamExt};

use self::blocked_ip::ForbiddenIpRepository;
use self::site::controller::create_site;
use self::site::domain::PingResult;
use self::site::infrastructure::SitePinger;
use self::site::repository::SiteRepository;

#[derive(Clone)]
struct AppState {
    pool: PgPool,
    site_repo: SiteRepository,
    forbidden_ip_repo: ForbiddenIpRepository,
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
        let pinger = SitePinger::new(&client);
        let repo = SiteRepository::new(pool);
        loop {
            ticker.tick().await;
            match repo.get_sites_for_ping(500).await {
                Ok(sites) => {
                    if sites.is_empty() {
                        continue;
                    }
                    println!("Fetched {} sites for ping...", sites.len());

                    let results: Vec<PingResult> = stream::iter(sites)
                        .map(|site| {
                            let pinger = pinger.clone();
                            async move {
                                let site_id = site.id.expect("site id required");
                                match pinger.ping(&site).await {
                                    Ok(resp) => PingResult {
                                        site_id,
                                        duration_ms: resp.ping_duration.as_secs_f64() * 1000.0,
                                        extra: serde_json::to_value(resp.extra).unwrap_or_default(),
                                    },
                                    Err(err) => PingResult {
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
                    if let Err(err) = repo.save_pings_batch(&results).await {
                        eprintln!("Error saving batch pings: {}", err);
                    } else {
                        println!("Successfully saved batch of {} pings", results.len());
                    }
                }
                Err(err) => {
                    eprintln!("Error fetching sites for ping: {}", err);
                }
            }
        }
    })
}
#[derive(Serialize)]
struct StatusResponse {
    status: &'static str,
    message: &'static str,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenv().expect(".env file not found");
    let port = env::var("PORT").unwrap_or_else(|_| "3000".to_string());
    let host = env::var("HOST").unwrap_or_else(|_| "127.0.0.1".to_string());
    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .unwrap();

    let app = Router::new()
        .route("/health", get(health_check))
        .route("/sites", get(get_all_sites))
        .route("/sites", post(create_site))
        .with_state(AppState {
            pool: pool.clone(),
            forbidden_ip_repo: blocked_ip::ForbiddenIpRepository::new(pool.clone()),
            site_repo: SiteRepository::new(pool.clone()),
        });
    let listner = tokio::net::TcpListener::bind(format!("{}:{}", host, port)).await?;
    check_all_sites(&pool).await;
    axum::serve(listner, app).await?;
    Ok(())
}

#[derive(Serialize, sqlx::FromRow)]
struct SiteRow {
    id: i64,
    user_id: String,
    url: String,
    created_at: chrono::DateTime<chrono::Utc>,
    last_check: Option<chrono::DateTime<chrono::Utc>>,
    status: String,
    status_updated_at: chrono::DateTime<chrono::Utc>,
    extra: Option<serde_json::Value>,
}

async fn get_all_sites(
    State(state): State<AppState>,
) -> Result<Json<Vec<SiteRow>>, (StatusCode, String)> {
    let sites = sqlx::query_as!(
        SiteRow,
        r#"
        SELECT 
            s.id, 
            s.user_id, 
            s.url, 
            s.created_at, 
            s.last_check, 
            s.status, 
            s.status_updated_at,
            p.extra
        FROM sites s
        LEFT JOIN LATERAL (
            SELECT extra
            FROM site_pings
            WHERE site_id = s.id
            ORDER BY time DESC
            LIMIT 1
        ) p ON true
        ORDER BY s.id
        "#
    )
    .fetch_all(&state.pool)
    .await
    .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    Ok(Json(sites))
}

async fn health_check() -> (StatusCode, Json<StatusResponse>) {
    let response = StatusResponse {
        status: "ok",
        message: "Uptime monitoring service is running",
    };
    (StatusCode::OK, Json(response))
}
