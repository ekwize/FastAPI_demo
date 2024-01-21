FROM python:3.10

RUN pip install poetry

RUN mkdir /booking

WORKDIR /booking

COPY poetry.lock pyproject.toml /booking/

RUN poetry install

COPY . .

RUN chmod a+x /booking/docker/*.sh

CMD ["poetry", "run", "gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8080"]










