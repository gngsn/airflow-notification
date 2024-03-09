CREATE TABLE users
(
    id   SERIAL NOT NULL,
    name VARCHAR,
    PRIMARY KEY (id)
);

alter table users
    add updated_at timestamp;

