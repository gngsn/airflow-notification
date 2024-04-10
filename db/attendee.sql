CREATE TABLE attendee
(
    meeting_id BIGINT,
    user_id    BIGINT,
    allowed    BOOLEAN   DEFAULT false,
    updated_at TIMESTAMP DEFAULT CLOCK_TIMESTAMP(),
    PRIMARY KEY (meeting_id, user_id)
);