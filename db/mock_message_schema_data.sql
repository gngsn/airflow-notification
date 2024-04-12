insert into message_schema (schedule, args, target, checksum)
values ('* * * * *', null,
        'SELECT u.id AS target, m.name AS meeting_name, m.end_time, (m.end_time - now())::time as remaining FROM users u join meeting m on u.id = m.host and m.start_time >= ''2024-04-09''::date and m.end_time <= ''2024-04-09''::date + interval ''5 days''',
        '');