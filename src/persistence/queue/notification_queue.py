from src.persistence.queue.base_queue import BaseQueue


class NotificationQueue(BaseQueue):
    """ Notification Queue DB Model """

    class Meta:
        table_name = 'notification_queue'

    @classmethod
    def insert_notification(cls, notification):
        cls.insert(
            notification.id,

        )
