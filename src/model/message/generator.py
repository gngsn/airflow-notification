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

            if not template or not _trigger_now(schema.schedule):
                """ The notification is not scheduled now """
                continue

            for args in _get_targets(schema):
                """ find target item to send notification """

                for users in _get_target_users(schema, args):
                    """ send notification to target user """
                    args = args | users
                    target_id = str(args["target"])

                    message = _to_message(template, args, target_id)
                    check_keys = _get_check_key(schema, args, target_id)

                    NotificationQueue.enqueue(check_keys, message.dict())


def _get_check_key(schema, args, target_id):
    check_keys = [args[key] for key in schema.check_keys.split(",")]
    unique_keys = [schema.template_id, target_id] + check_keys

    return ":".join(unique_keys)


def _to_message(template: MessageTemplate, args: dict, target_id: str) -> Message:
    formed = replace(template.message, args)
    return Message(title=template.title, body=formed, to=target_id)


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
