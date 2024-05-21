import json

from src.persistence.queue.base_queue import BaseQueue


class NotificationQueue(BaseQueue):
    """ Notification Queue DB Model """

    class Meta:
        table_name = 'notification_queue'

    @classmethod
    def enqueue(cls, queue_checksum: str, message: dict):
        cls.insert(
            checksum=queue_checksum,
            playload=json.dumps(message)
        )
