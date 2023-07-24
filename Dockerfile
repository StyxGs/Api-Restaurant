FROM python:3.11-alpine3.18
RUN pip install poetry
WORKDIR /task
COPY poetry.lock pyproject.toml /task/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY . .
RUN chmod a+x *.sh
CMD ["sh", "app.sh"]