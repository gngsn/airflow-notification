from psycopg2 import pool
from psycopg2.extras import RealDictCursor


def getpool(host, name, user, password):
    db_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host=host,
        dbname=name,
        user=user,
        password=password
    )


def getconn(db_pool):
    connection = db_pool.getconn()
    db_conn = connection.cursor(cursor_factory=RealDictCursor)  # Use RealDictCursor for dictionary-like results
    try:
        yield db_conn
    finally:
        db_conn.close()
        db_pool.putconn(connection)


pool = getpool()
conn = getconn(pool)
