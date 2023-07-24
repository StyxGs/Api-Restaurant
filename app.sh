#!/bin/bush

alembic revision --autogenerate -m 'init'

alembic upgrade +1

uvicorn src.api.__main__:app --host 0.0.0.0 --port 80