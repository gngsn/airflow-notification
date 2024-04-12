CREATE TABLE message_schema
(
    id         BIGSERIAL,
    schedule   VARCHAR(100),
    args       VARCHAR(1000),
    target     VARCHAR(1000),
    checksum   VARCHAR(200),
    updated_at TIMESTAMP DEFAULT CLOCK_TIMESTAMP(),
    PRIMARY KEY (id)
);

