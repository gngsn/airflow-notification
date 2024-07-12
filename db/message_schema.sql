CREATE TABLE message_schema
(
    id            BIGSERIAL,
    template_id   VARCHAR(50),
    schedule      VARCHAR(100),
    args          VARCHAR(1000),
    target_db     VARCHAR(100),
    target_items  TEXT,
    target_users  TEXT,
    checksum_keys VARCHAR(200),
    updated_at    TIMESTAMP DEFAULT CLOCK_TIMESTAMP(),
    PRIMARY KEY (id)
);

INSERT INTO public.message_schema (id,
                                   template_id,
                                   schedule,
                                   args,
                                   target_db,
                                   target_items,
                                   target_users,
                                   checksum_keys)
VALUES (1, 'UMSV10001', '* * * * *',
        '{}',
        'AURORA_ADM',
        'SELECT * FROM meeting WHERE now() BETWEEN start_time - INTERVAL ''30 minutes'' AND start_time + INTERVAL ''30 minutes''',
        'SELECT u.id AS target, m.name AS meeting_name, m.end_time, (m.end_time - now())::time as remaining FROM users u join meeting m on u.id = m.host and m.start_time >= ''2024-04-09''::date and m.end_time <= ''2024-04-09''::date + interval ''5 days''',
        '');
