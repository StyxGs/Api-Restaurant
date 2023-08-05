import os

from dotenv import load_dotenv

from src.infrastructure.db.congif.moleds.db import DBConfig, RedisConfig


def get_env(path_env: str):
    dotenv_path_test = os.path.join(os.path.dirname(__file__), path_env)
    load_dotenv(dotenv_path=dotenv_path_test)


def load_data_db(path_env: str) -> dict:
    get_env(path_env)
    user: str | None = os.environ.get('POSTGRES_USER')
    password: str | None = os.environ.get('POSTGRES_PASSWORD')
    host: str | None = os.environ.get('POSTGRES_HOST')
    port: str | None = os.environ.get('POSTGRES_PORT')
    name: str | None = os.environ.get('POSTGRES_DB')
    return dict(user=user, password=password, host=host, port=port, name=name)


def load_db_config(path_env: str | None = None) -> DBConfig:
    if not path_env:
        path_env = '../../../config_env/.env'
    return DBConfig(**load_data_db(path_env))


def load_data_redis(path_env: str) -> dict:
    get_env(path_env)
    host: str | None = os.environ.get('REDIS_HOST')
    port: str | None = os.environ.get('REDIS_PORT')
    return dict(host=host, port=port)


def load_redis_config(path_env: str | None = None) -> RedisConfig:
    if not path_env:
        path_env = '../../../config_env/.env'
    return RedisConfig(**load_data_redis(path_env))
