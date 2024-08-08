def row_to_json(cursor):
    """ Convert retrieved database rows to json """
    for row in cursor.fetchall():
        yield {column[0]: str(value) for column, value in zip(cursor.description, row)}
