mod site;
use std::env;
use std::time::Duration;

use axum::Json;
use axum::{Router, http::StatusCode, routing::get};
use dotenvy::dotenv;
use serde::Serialize;
use tokio::task::JoinHandle;
use tokio::time::interval;

async fn check_all_sites() -> JoinHandle<()> {
    tokio::spawn(async move {
        let mut ticker = interval(Duration::from_secs(10));
        loop {
            ticker.tick().await;
            println!("CRON")
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
    let pool = sqlx::postgres::PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .unwrap();

    let app = Router::new()
        .route("/health", get(health_check))
        .with_state(pool);
    let listner = tokio::net::TcpListener::bind(format!("{}:{}", host, port)).await?;
    check_all_sites();
    axum::serve(listner, app).await?;
    Ok(())
}
async fn health_check() -> (StatusCode, Json<StatusResponse>) {
    let response = StatusResponse {
        status: "ok",
        message: "Uptime monitoring service is running",
    };
    (StatusCode::OK, Json(response))
}
