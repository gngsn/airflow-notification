CREATE TABLE db_connection
(
    id         VARCHAR(50),
    dbms       VARCHAR(50),
    host       VARCHAR(255),
    database   VARCHAR(100),
    port       INT,
    username   VARCHAR(100),
    password   VARCHAR(255),
    updated_at TIMESTAMP DEFAULT CLOCK_TIMESTAMP(),
    PRIMARY KEY (id)
);

insert into db_connection (id, dbms, host, database, port, username, password)
values ('AURORA_ADM', 'postgresql', 'localhost', 'ums', 5678, 'postgres', 'postgres');