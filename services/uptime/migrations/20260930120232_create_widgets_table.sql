CREATE TABLE IF NOT EXISTS widgets (
    id SMALLSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_widgets_name ON widgets (name);

INSERT INTO widgets (name) VALUES
    ('badge'),
    ('stat'),
    ('gauge'),
    ('sparkline'),
    ('key_value'),
    ('chart'),
    ('row'),
    ('column'),
    ('text')
ON CONFLICT (name) DO NOTHING;
