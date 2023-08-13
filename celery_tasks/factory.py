from celery import Celery

from celery_tasks.tasks.config.config import CeleryConfig


def create_celery(config: CeleryConfig):
    return Celery('celery_tasks', broker=config.get_url_broker)
