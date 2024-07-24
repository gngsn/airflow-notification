import json
from typing import Generator

import pendulum
from croniter import croniter

from src.lib.template import replace
from src.model.message.message import Message
from src.persistence import init_pg
from src.persistence.base import execute, transactional
from src.persistence.base.connection import Connector
from src.persistence.entity.external_connector import ExternalDbConnection
from src.persistence.entity.schema import MessageSchema
from src.persistence.entity.template import MessageTemplate
from src.persistence.queue.notification_queue import NotificationQueue


def _init():
    init_pg()


def run(_setup=_init):
    _setup()
    _generate()


def _generate():
    for schema in MessageSchema.select_all():
        connection = ExternalDbConnection.get_target_db_connection(schema)

        with Connector(connection):
            template_id = schema.template_id
            template = MessageTemplate.find_one(template_id)

            if not _trigger_now(schema.schedule) or not template:
                """ The notification is not scheduled now """
                continue

            for args in _get_targets(schema):
                for users in _get_target_users(schema, args):
                    args = args | users
                    target_id = str(args["target"])

                    formed = replace(template.message, args)
                    message = Message(title=template.title, body=formed, to=target_id)
                    notification_checksums = [args[key] for key in schema.checksum_keys.split(",")]

                    queue_checksum = _make_checksum(schema.template_id, target_id, notification_checksums)
                    NotificationQueue.enqueue(queue_checksum, message.dict())


def _make_checksum(template_id: str, target: str, checksums: list[str]):
    return ":".join([template_id, target] + checksums)


def row_to_json(cursor):
    """ Convert retrieved database rows to json """
    for row in cursor.fetchall():
        yield {column[0]: str(value) for column, value in zip(cursor.description, row)}


@transactional
def _get_targets(schema: MessageSchema) -> Generator:
    """ Get targets by executing schema's target properties which is a sql query """

    targets = replace(schema.get_targets(), json.loads(schema.args))
    cursor = execute(targets)
    return row_to_json(cursor)


def _get_target_users(schema: MessageSchema, args: dict) -> Generator:
    """ Get users to be sent by executing target_users properties which is a sql query """

    users = replace(schema.target_users, args | json.loads(schema.args))
    cursor = execute(users)
    return row_to_json(cursor)


def _trigger_now(schedule, now=pendulum.now(tz="Asia/Seoul")) -> bool:
    return croniter.match(schedule, now)


if __name__ == "__main__":
    run()
