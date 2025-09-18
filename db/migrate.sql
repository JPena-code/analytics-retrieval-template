-- If the user that is assigned to connect with the database does not have
-- the required permissions to create the extension, or DDL commands, you
-- will need to send these commands to your DBA or hosting provider.

-- BE sure that you are in your target database before running
CREATE EXTENSION IF NOT EXISTS "timescaledb";

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

BEGIN;
    CREATE SCHEMA IF NOT EXISTS analytics;

    CREATE TABLE analytics.events (
        id SERIAL NOT NULL,
        time TIMESTAMPTZ WITH TIME ZONE NOT NULL DEFAULT NOW()
        req_id UUID NOT NULL,
        page VARCHAR(256) NOT NULL,
        agent VARCHAR( NOT NULL,
        ip_address BIGINT NOT NULL,
        referrer VARCHAR,
        session_id VARCHAR,
        duration FLOAT NOT NULL,
        PRIMARY KEY (id, time)
    );

COMMIT;
