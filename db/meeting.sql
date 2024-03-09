CREATE TABLE meeting
(
    id         SERIAL NOT NULL,
    room       VARCHAR,
    owner      VARCHAR,
    start_time TIMESTAMP DEFAULT NOW(),
    end_time   TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id)
);

alter table meeting
    add updated_at timestamp;

alter table meeting
    add name varchar(255);

