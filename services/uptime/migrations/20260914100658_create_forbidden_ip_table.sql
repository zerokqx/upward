CREATE TABLE IF NOT EXISTS forbidden_ip (
    id BIGSERIAL PRIMARY KEY,
    ip TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_forbidden_ip_ip ON forbidden_ip (ip);
