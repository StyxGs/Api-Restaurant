from asyncio import get_event_loop

from celery_tasks.factory import create_celery
from celery_tasks.tasks.config.config import load_celery_config
from celery_tasks.tasks.task_admin import main_func_admin

celery_app = create_celery(load_celery_config())

celery_app.conf.beat_schedule = {
    'add_data_to_db': {
        'task': 'admin',
        'schedule': 15.0,
    }
}


@celery_app.task(name='admin')
def task_admin() -> str:
    loop = get_event_loop()
    result: str = loop.run_until_complete(main_func_admin())
    return result


if __name__ == '__main__':
    celery_app.start()
