from typing import Generator

import pendulum
from croniter import croniter

from src.lib.template import replace
from src.model.message.message import Message
from src.persistence import init_pg
from src.persistence.base import execute, transactional
from src.persistence.base.connection import Connector
from src.persistence.entity.schema import MessageSchema
from src.persistence.entity.template import MessageTemplate
from src.persistence.queue.notification_queue import NotificationQueue


def _init():
    init_pg()


def run(setup=_init):
    setup()
    for s in MessageSchema.select_all():
        with Connector(s.get_target_db_connection()):
            template = MessageTemplate.find_one(s.template_id)

            if not _trigger_now(s.schedule) or not template:
                """ The notification is not scheduled now """
                continue

            for args in _get_targets(s):
                substitute = replace(template.message, args)

                target_id = args["target"]
                message = Message(title=template.title, body=substitute, to=target_id)
                notification_checksums = [args[key] for key in s.checksum_keys.split(",")]

                queue_checksum = _make_checksum(s.template_id, target_id, notification_checksums)
                NotificationQueue.enqueue(queue_checksum, message)


def _make_checksum(template_id: str, target: str, checksums: list[str]):
    return ":".join([template_id, target, checksums])


@transactional
def _get_targets(schema: MessageSchema) -> Generator:
    """ Get targets by executing schema's target properties which is a sql """

    def row_to_json(cursor):
        """ Convert retrieved database rows to json """
        for row in cursor.fetchall():
            yield {column[0]: value for column, value in zip(cursor.description, row)}

    cursor = execute(schema.target)
    return row_to_json(cursor)


def _trigger_now(schedule, now=pendulum.now(tz="Asia/Seoul")) -> bool:
    return croniter.match(schedule, now)
