from typing import Generator

import pendulum
from croniter import croniter

from src.persistence.base import execute, transactional
from src.persistence.base import init_pg
from src.persistence.model.schema import MessageSchema
from src.persistence.model.template import MessageTemplate


def run():
    @transactional
    def get_targets(schema: MessageSchema) -> Generator:
        """ Get targets by executing schema's target properties which is a sql """

        def row_to_json(cursor):
            """ Convert retrieved database rows to json """
            for row in cursor.fetchall():
                yield {column[0]: value for column, value in zip(cursor.description, row)}

        cursor = execute(schema.target)
        return row_to_json(cursor)

    def match(schedule, now=pendulum.now(tz="Asia/Seoul")) -> bool:
        return croniter.match(schedule, now)

    def replace(_templates, target):
        from string import Template

        return Template(_templates.message).substitute(**target)

    def match_one(list, key):
        it = [l for l in list if l.id == key]
        return it.pop() if len(it) != 0 else None

    init_pg()

    messages = []

    message_templates = MessageTemplate.find_all()

    for s in MessageSchema.select_all():
        template = match_one(message_templates, s.template_id)

        if match(s.schedule) and template:
            """ Messages scheduled now """
            for args in get_targets(s):
                substitute = replace(template, args)
                messages.append(substitute)

    return messages
