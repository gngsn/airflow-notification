CREATE TABLE meeting
(
    id         SERIAL NOT NULL,
    host       BIGINT,
    room       VARCHAR(100),
    name       VARCHAR(255),
--     date       DATE,
    start_time TIMESTAMP,
    end_time   TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CLOCK_TIMESTAMP(),
    PRIMARY KEY (id)
);