CREATE TABLE message_schema
(
    id            BIGSERIAL,
    template_id   VARCHAR(50),
    schedule      VARCHAR(100),
    args          VARCHAR(1000),
    target        VARCHAR(1000),
    checksum_keys VARCHAR(200),
    updated_at    TIMESTAMP DEFAULT CLOCK_TIMESTAMP(),
    PRIMARY KEY (id)
);

