FROM rust:1.89-bookworm AS builder

WORKDIR /app
COPY services/identify/Cargo.toml services/identify/Cargo.lock ./
COPY services/identify/.sqlx ./.sqlx
COPY services/identify/src ./src
ENV SQLX_OFFLINE=true
RUN cargo build --release
RUN cargo install sqlx-cli --version 0.8.6 --no-default-features --features rustls,postgres

FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /app/target/release/identify /usr/local/bin/identify
COPY --from=builder /usr/local/cargo/bin/sqlx /usr/local/bin/sqlx
COPY services/identify/migrations /app/migrations

ENV HOST=0.0.0.0
ENV PORT=3001

EXPOSE 3001
CMD ["sh", "-c", "sqlx migrate run --source /app/migrations && exec identify"]
