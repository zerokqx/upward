FROM rust:1.80-slim AS builder
WORKDIR /app
COPY . .
RUN cargo build --release --bin uptime

FROM gcr.io/distroless/cc-debian12
WORKDIR /app

COPY --from=builder /app/target/release/uptime /app/uptime

EXPOSE 3000
CMD ["/app/uptime"]
