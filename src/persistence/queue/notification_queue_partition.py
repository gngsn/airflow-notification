from pendulum import now, date

from src.persistence import execute
from src.persistence.queue import NotificationQueue, NOTIFICATION_QUEUE_TABLE_NAME

PARTITION_FORMAT = "YYYY_MM_DD"


def create_partition_if_not_exists(now_date=now().date()):
    table_name = NOTIFICATION_QUEUE_TABLE_NAME
    partition_name = NotificationQueue.get_partition_name(now_date)

    cursor = execute(f"""
        SELECT
            parent.relname      AS parent,
            child.relname       AS child
        FROM pg_inherits
            JOIN pg_class parent            ON pg_inherits.inhparent = parent.oid
            JOIN pg_class child             ON pg_inherits.inhrelid   = child.oid
        WHERE parent.relname='{table_name}' and child.relname='{partition_name}';
        """)

    if cursor.rowcount != 0:
        return

    execute(f"""
        CREATE TABLE {partition_name}
        PARTITION OF {table_name}
        FOR VALUES FROM ('{now_date}') TO ('{now_date.add(days=1)}')""")


if __name__ == "__main__":
    create_partition_if_not_exists(date(year=2024, month=5, day=23))
