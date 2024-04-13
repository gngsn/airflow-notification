from typing import Generator

import pendulum

from src.domain.message.message import Message
from src.domain.message_queue import MessageQueue
from src.persistence.base import execute, transactional
from src.persistence.base import init_pg
from src.persistence.model.schema import MessageSchema
from src.persistence.model.template import MessageTemplate


def _init():
    init_pg()


def run(setup=_init):
    setup()
    message_templates = MessageTemplate.find_all()

    for s in MessageSchema.select_all():
        template = _match_one(message_templates, s.template_id)

        if _trigger_now(s.schedule) and template:
            """ Messages scheduled now """
            for args in _get_targets(s):
                substitute = _replace(template.message, args)
                MessageQueue.append(
                    Message(
                        title=template.title,
                        body=substitute,
                        to=args['target']
                    )
                )


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
    from croniter import croniter
    return croniter.match(schedule, now)


def _replace(template, target):
    from string import Template

    return Template(template).substitute(**target)


def _match_one(list, key):
    it = [l for l in list if l.id == key]
    return it.pop() if len(it) != 0 else None
