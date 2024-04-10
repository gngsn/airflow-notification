CREATE TABLE meeting
(
    id         SERIAL NOT NULL,
    room       VARCHAR(100),
    name       VARCHAR(255),
    owner      VARCHAR(100),
    start_time TIMESTAMP,
    end_time   TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CLOCK_TIMESTAMP(),
    PRIMARY KEY (id)
);

