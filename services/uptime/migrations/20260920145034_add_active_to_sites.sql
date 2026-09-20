-- Add active column to sites table with default false
ALTER TABLE sites ADD COLUMN IF NOT EXISTS active BOOLEAN NOT NULL DEFAULT FALSE;
