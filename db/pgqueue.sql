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

CREATE TABLE ums_queue
(
) INHERITS (base_queue);

-- insert into ums_queue(params) values (<YOUR BUSINESS PAYLOAD JSON>)
-- and priority = <REQUIRED PROIRITY>
--   and try_count <= max_tries;


-- select * from <YOUR QUEUE NAME> where status = 0
-- limit 1
-- for update skip locked;