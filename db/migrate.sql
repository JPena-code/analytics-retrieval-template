-- If the user that is assigned to connect with the database does not have
-- the required permissions to create the extension, or DDL commands, you
-- will need to send these commands to your DBA or hosting provider.

-- BE sure that you are in your target database before running
CREATE EXTENSION IF NOT EXISTS "timescaledb";

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

BEGIN;
    CREATE SCHEMA IF NOT EXISTS analytics;

    CREATE SEQUENCE IF NOT EXISTS analytics.events_id_seq;

    CREATE TABLE analytics.events (
        id SERIAL NOT NULL DEFAULT nextval('analytics.events_id_seq'),
        time TIMESTAMPTZ WITH TIME ZONE NOT NULL DEFAULT NOW()
        page VARCHAR(256) NOT NULL,
        agent VARCHAR NOT NULL,
        ip_address INET NOT NULL,
        referrer VARCHAR,
        session_id VARCHAR,
        duration FLOAT NOT NULL,
        PRIMARY KEY (id, time)
    )
    WITH (
        tsdb.hypertable,
        tsdb.partition_column = 'time',
        tsdb.segmentby = 'page',
        tsdb.chunk_interval = INTERVAL '7 days'
    );

    -- Improve query performance for filtering by page and ordering by time
    -- leveraging timesacle partition core system
    CREATE INDEX page_time_desc ON analytics.events (page, 'time' DESC);

COMMIT;
