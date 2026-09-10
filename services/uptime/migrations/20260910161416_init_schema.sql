CREATE TABLE IF NOT EXISTS sites (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS site_pings (
    time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    site_id BIGINT NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
    duration_ms DOUBLE PRECISION NOT NULL,
    extra JSONB
);

SELECT create_hypertable('site_pings', 'time', if_not_exists => TRUE);
