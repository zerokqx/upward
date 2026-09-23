mod blocked_ip;
mod domain;
mod openapi;
mod ping;
mod server;
mod site;

use dotenvy::dotenv;
use reqwest::redirect;
use sqlx::PgPool;
use sqlx::postgres::PgPoolOptions;
use std::env;
use std::net::SocketAddr;
use std::time::Duration;
use tokio::task::JoinHandle;
use tokio::time::interval;
use tracing::{Level, error, info};
use tracing_subscriber::FmtSubscriber;

use futures::stream::{self, StreamExt};

use self::blocked_ip::ForbiddenIpRepository;
use self::domain::SiteId;
use self::ping::domain::PingRecord;
use self::ping::infrastructure::HttpPinger;
use self::ping::repository::PingRepository;
use self::site::controller::IpValidator;
use self::site::domain::Site;
use self::site::repository::{ChallengeRepository, SiteRepository};

#[derive(Clone)]
pub struct AppState {
    pub pool: PgPool,
    pub site_repo: SiteRepository,
    pub ping_repo: PingRepository,
    pub forbidden_ip_repo: ForbiddenIpRepository,
    pub redis: redis::aio::MultiplexedConnection,
    pub challenge_repo: ChallengeRepository,
}

async fn check_single_site(site: Site, validator: &IpValidator, pinger: &HttpPinger) -> PingRecord {
    let site_id = site.id.expect("site id required");

    if let Err(err) = validator.validate_url(site.url.as_ref()).await {
        return PingRecord {
            site_id,
            duration_ms: 0.0,
            extra: serde_json::json!({
                "error": format!("Security validation failed: {err}")
            }),
        };
    }

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

#[derive(Clone, Copy, Debug)]
pub struct WorkerConfig {
    pub batch_size: i64,
    pub concurrency: usize,
}

impl WorkerConfig {
    pub fn from_env() -> Self {
        let batch_size = env::var("PING_BATCH_SIZE")
            .ok()
            .and_then(|v| v.parse().ok())
            .unwrap_or(500);

        let concurrency = env::var("PING_CONCURRENCY")
            .ok()
            .and_then(|v| v.parse().ok())
            .unwrap_or(25);

        Self {
            batch_size,
            concurrency,
        }
    }
}

async fn process_batch(
    state: &AppState,
    validator: &IpValidator,
    pinger: &HttpPinger,
    config: WorkerConfig,
) {
    let sites = match state.site_repo.get_sites_for_ping(config.batch_size).await {
        Ok(sites) => sites,
        Err(err) => {
            error!("Error fetching sites for ping: {err}");
            return;
        }
    };

    if sites.is_empty() {
        return;
    }

    info!("Fetched {} sites for ping...", sites.len());

    let results: Vec<PingRecord> = stream::iter(sites)
        .map(|site| {
            let pinger = pinger.clone();
            let validator = validator.clone();
            async move { check_single_site(site, &validator, &pinger).await }
        })
        .buffer_unordered(config.concurrency)
        .collect()
        .await;

    info!("Pings completed, saving {} results...", results.len());
    if let Err(err) = state.ping_repo.save_pings_batch(&results).await {
        error!("Error saving batch pings: {err}");
    } else {
        info!("Successfully saved batch of {} pings", results.len());
    }

    let site_ids: Vec<SiteId> = results.iter().map(|r| r.site_id).collect();
    if let Err(err) = state.site_repo.mark_sites_idle(&site_ids).await {
        error!("Error updating sites status: {err}");
    }
}

fn spawn_uptime_worker(state: AppState, config: WorkerConfig) -> JoinHandle<()> {
    tokio::spawn(async move {
        info!(
            "Starting uptime worker (batch_size={}, concurrency={})",
            config.batch_size, config.concurrency
        );
        let mut ticker = interval(Duration::from_secs(10));
        let client = reqwest::ClientBuilder::new()
            .user_agent("UptimeMonitor/1.0")
            .redirect(redirect::Policy::none())
            .timeout(Duration::from_secs(10))
            .build()
            .unwrap();
        let pinger = HttpPinger::new(&client);
        let validator = IpValidator::new(state.forbidden_ip_repo.clone());

        loop {
            ticker.tick().await;
            process_batch(&state, &validator, &pinger, config).await;
        }
    })
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenv().expect(".env file not found");
    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::DEBUG)
        .finish();
    tracing::subscriber::set_global_default(subscriber).expect("setting default subscriber failed");

    let port: u16 = env::var("PORT")
        .unwrap_or_else(|_| "3000".to_string())
        .parse()?;
    let host = env::var("HOST").unwrap_or_else(|_| "127.0.0.1".to_string());
    let addr: SocketAddr = format!("{}:{}", host, port).parse()?;

    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .unwrap();

    let redis_url = env::var("REDIS_URL").unwrap_or_else(|_| "redis://127.0.0.1:6379".to_string());
    let redis_client = redis::Client::open(redis_url)?;
    let redis_conn = redis_client.get_multiplexed_async_connection().await?;
    let challenge_repo = ChallengeRepository::new(redis_conn.clone());

    let state = AppState {
        pool: pool.clone(),
        forbidden_ip_repo: blocked_ip::ForbiddenIpRepository::new(pool.clone()),
        site_repo: SiteRepository::new(pool.clone()),
        ping_repo: PingRepository::new(pool.clone()),
        redis: redis_conn,
        challenge_repo,
    };

    let worker_config = WorkerConfig::from_env();
    let _checker_handle = spawn_uptime_worker(state.clone(), worker_config);

    server::run_server(addr, state).await?;
    Ok(())
}
