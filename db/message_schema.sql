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
        'SELECT id AS meeting_id, start_time AS start_time FROM meeting WHERE now() BETWEEN start_time - INTERVAL ''30 minutes'' AND start_time + INTERVAL ''30 minutes''',
        'SELECT u.id AS target
FROM users u JOIN attendee a ON u.id = a.user_id
WHERE a.meeting_id = $meeting_id AND a.accepted = true',
        'meeting_id,start_time');
