import os
from dataclasses import dataclass

from src.common.congif.db import get_env


@dataclass
class CeleryConfig:
    user: str
    password: str
    port: str
    host: str

    @property
    def get_url_broker(self):
        return f'amqp://{self.user}:{self.password}@{self.host}:{self.port}//'


def load_data_celery(path_env: str) -> dict:
    get_env(path_env)
    user: str | None = os.environ.get('RABBITMQ_DEFAULT_USER')
    password: str | None = os.environ.get('RABBITMQ_DEFAULT_PASS')
    port: str | None = os.environ.get('RABBITMQ_DEFAULT_PORT')
    host: str | None = os.environ.get('RABBITMQ_DEFAULT_HOST')
    return dict(user=user, password=password, host=host, port=port)


def load_celery_config(path_env: str | None = None) -> CeleryConfig:
    if not path_env:
        path_env = '../../../config_env/.env'
    return CeleryConfig(**load_data_celery(path_env))
