from pq import PQ
from procrastinate import PsycopgConnector, App
# Make an app in your code
# app = App(connector=SyncPsycopgConnector())
from psycopg2 import connect

# dbh = init_pg()

conn = connect('dbname=example user=postgres')
pq = PQ(conn)

pq.create()

queue = pq['default']


@queue.task(schedule_at='1h')
def eat(job_id, kind):
    print('umm, %s apples taste good.' % kind)


eat('Cox')
queue.work()

app = App(
    connector=PsycopgConnector(
        kwargs={
            "host": "localhost:5434",
            "user": "postgres",
            "password": "postgres",
        }
    )
)
