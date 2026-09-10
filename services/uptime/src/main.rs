use self::site::{Site, UserId};

mod site;

#[tokio::main]
async fn main() {
    let google = Site::new("https://samuraiworld.site/api/info".to_string(), UserId("dwad".to_string()));

    let ping = google.ping().await.unwrap();
    println!("Hello, world! {:#?}", ping);
}
