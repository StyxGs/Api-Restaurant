FROM python:3.10-slim
RUN pip install poetry
WORKDIR /task
COPY poetry.lock pyproject.toml /task/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY . .
