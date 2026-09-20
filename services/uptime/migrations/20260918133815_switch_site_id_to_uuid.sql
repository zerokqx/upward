-- Switch SiteId from BIGINT to UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

ALTER TABLE site_pings DROP CONSTRAINT IF EXISTS site_pings_site_id_fkey;
ALTER TABLE sites DROP CONSTRAINT IF EXISTS sites_pkey CASCADE;

ALTER TABLE sites ADD COLUMN new_id UUID DEFAULT gen_random_uuid();
UPDATE sites SET new_id = gen_random_uuid() WHERE new_id IS NULL;

ALTER TABLE site_pings ADD COLUMN new_site_id UUID;
UPDATE site_pings p SET new_site_id = s.new_id FROM sites s WHERE p.site_id = s.id;

ALTER TABLE sites DROP COLUMN id;
ALTER TABLE sites RENAME COLUMN new_id TO id;
ALTER TABLE sites ALTER COLUMN id SET NOT NULL;
ALTER TABLE sites ADD PRIMARY KEY (id);

ALTER TABLE site_pings DROP COLUMN site_id;
ALTER TABLE site_pings RENAME COLUMN new_site_id TO site_id;
ALTER TABLE site_pings ALTER COLUMN site_id SET NOT NULL;

ALTER TABLE site_pings ADD CONSTRAINT site_pings_site_id_fkey FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE;
