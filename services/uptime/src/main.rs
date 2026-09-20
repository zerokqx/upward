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
use tracing::Level;
use tracing_subscriber::FmtSubscriber;

use futures::stream::{self, StreamExt};

use self::blocked_ip::ForbiddenIpRepository;
use self::domain::SiteId;
use self::ping::domain::PingRecord;
use self::ping::infrastructure::HttpPinger;
use self::ping::repository::PingRepository;
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

fn check_all_sites(
    pool: &PgPool,
    forbidden_ip_repo: ForbiddenIpRepository,
) -> JoinHandle<()> {
    let pool = pool.clone();
    tokio::spawn(async move {
        let mut ticker = interval(Duration::from_secs(10));
        let client = reqwest::ClientBuilder::new()
            .user_agent("UptimeMonitor/1.0")
            .redirect(redirect::Policy::none())
            .timeout(Duration::from_secs(10))
            .build()
            .unwrap();
        let pinger = HttpPinger::new(&client);
        let site_repo = SiteRepository::new(pool.clone());
        let ping_repo = PingRepository::new(pool);
        let validator = site::controller::IpValidator::new(forbidden_ip_repo);

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
                            let validator = validator.clone();
                            async move {
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

    let _checker_handle = check_all_sites(&pool, state.forbidden_ip_repo.clone());

    server::run_server(addr, state).await?;
    Ok(())
}
