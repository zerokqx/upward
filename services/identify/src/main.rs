mod domain;
mod login;
mod oauth;
mod openapi;
mod server;
mod services;

pub use domain::{AccessToken, RefreshToken};

use sqlx::PgPool;
use sqlx::postgres::PgPoolOptions;
use std::env;
use std::net::SocketAddr;
use std::sync::Arc;
use tracing::Level;
use tracing_subscriber::FmtSubscriber;

use self::login::UserRepository;
use self::services::JwtService;

#[derive(Clone)]
pub struct AppState {
    pub pool: PgPool,
    pub user_repo: Arc<UserRepository>,
    pub redis: redis::aio::MultiplexedConnection,
    pub jwt_service: JwtService,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenvy::dotenv().ok();

    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::DEBUG)
        .finish();
    let _ = tracing::subscriber::set_global_default(subscriber);

    let port: u16 = env::var("PORT")
        .unwrap_or_else(|_| "3001".to_string())
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

    let private_key_pem = load_key_file("JWT_PRIVATE_KEY_PATH", "certs/private.pem")
        .expect("Не удалось прочитать приватный ключ JWT (certs/private.pem). Сгенерируйте ключи через: moon run identify:gen-keys");
    let public_key_pem = load_key_file("JWT_PUBLIC_KEY_PATH", "certs/public.pem")
        .expect("Не удалось прочитать публичный ключ JWT (certs/public.pem).");

    let jwt_service = JwtService::new(&private_key_pem, &public_key_pem)
        .expect("Не удалось инициализировать JwtService с переданной парой RSA ключей");

    let state = AppState {
        pool: pool.clone(),
        user_repo: Arc::new(UserRepository::new(pool.clone())),
        redis: redis_conn,
        jwt_service,
    };

    server::run_server(addr, state).await?;
    Ok(())
}

fn load_key_file(env_var: &str, default_path: &str) -> Result<String, std::io::Error> {
    let path_str = env::var(env_var).unwrap_or_else(|_| default_path.to_string());
    let path = std::path::Path::new(&path_str);
    if path.exists() {
        return std::fs::read_to_string(path);
    }
    let fallback = std::path::Path::new("services/identify").join(path);
    if fallback.exists() {
        return std::fs::read_to_string(fallback);
    }
    std::fs::read_to_string(path)
}

