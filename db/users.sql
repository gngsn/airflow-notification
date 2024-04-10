create table users
(
    id         INT,
    first_name VARCHAR(100),
    last_name  VARCHAR(100),
    email      VARCHAR(500),
    gender     VARCHAR(50),
    ip_address VARCHAR(20),
    created_at TIMESTAMP DEFAULT CLOCK_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CLOCK_TIMESTAMP(),
    PRIMARY KEY (id)
);