CREATE TABLE attendee
(
    meeting_id BIGINT,
    user_id    BIGINT,
    accepted   BOOLEAN   DEFAULT false,
    updated_at TIMESTAMP DEFAULT CLOCK_TIMESTAMP(),
    PRIMARY KEY (meeting_id, user_id)
);


insert into public.attendee (meeting_id, user_id, accepted)
values (14, 19, true);
