CREATE TABLE meeting
(
    id         SERIAL NOT NULL,
    room       VARCHAR,
    owner      VARCHAR,
    start_time TIMESTAMP DEFAULT NOW(),
    end_time   TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id)
)