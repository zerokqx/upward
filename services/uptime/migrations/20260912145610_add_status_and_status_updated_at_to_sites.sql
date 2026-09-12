ALTER TABLE sites
ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'idle',
ADD COLUMN IF NOT EXISTS status_updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

CREATE INDEX IF NOT EXISTS idx_sites_status_last_check ON sites (status, last_check ASC NULLS FIRST);
CREATE INDEX IF NOT EXISTS idx_sites_status_updated_at ON sites (status_updated_at) WHERE status = 'processing';
