FROM python:3.9.9-slim as builder
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && \
    apt install gcc build-essential -y --no-install-recommends

COPY ./requirements.txt requirements.txt
RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM python:3.9.9-slim
WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip3 install --no-cache -U pip
RUN pip3 install --no-cache /wheels/*
