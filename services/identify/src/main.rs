mod openapi;
mod server;

use std::env;
use std::net::SocketAddr;
use tracing::Level;
use tracing_subscriber::FmtSubscriber;

#[derive(Clone)]
pub struct AppState {}

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

    let state = AppState {};

    server::run_server(addr, state).await?;
    Ok(())
}
