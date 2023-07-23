from src.infrastructure.db.congif.moleds.db import DBConfig


def load_data_db() -> dict:
    import os

    from dotenv import load_dotenv
    dotenv_path_test = os.path.join(os.path.dirname(__file__), '../../../config_env/.env')
    load_dotenv(dotenv_path=dotenv_path_test)
    user: str = os.environ.get('POSTGRES_USER')
    password: str = os.environ.get('POSTGRES_PASSWORD')
    host: str = os.environ.get('POSTGRES_HOST')
    port: str = os.environ.get('POSTGRES_PORT')
    name: str = os.environ.get('POSTGRES_DB')
    return dict(user=user, password=password, host=host, port=port, name=name)


def load_db_config() -> DBConfig:
    return DBConfig(**load_data_db())
