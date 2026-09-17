-- Retention policy for site_pings: automatically drop data older than 30 days
SELECT add_retention_policy('site_pings', INTERVAL '30 days', if_not_exists => TRUE);
