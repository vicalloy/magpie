FROM python:3.11

RUN pip install --upgrade poetry

RUN mkdir /app
WORKDIR /app

COPY ./ ./

RUN poetry config virtualenvs.create false
RUN poetry install --only=main,telegram
