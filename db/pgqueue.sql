-- https://dev.to/mikevv/simple-queue-with-postgresql-1ngc

CREATE TABLE base_queue
(
    id          serial                              NOT NULL,
    status      integer   DEFAULT 0                 NOT NULL,
    try_count   integer   DEFAULT 0                 NOT NULL,
    max_tries   integer   DEFAULT 5                 NOT NULL,
    params      json,
    create_time timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_time timestamp,
    priority    integer   DEFAULT 0                 NOT NULL
);
