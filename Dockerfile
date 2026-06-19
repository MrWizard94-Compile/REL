FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    REL_PATH=/app/runtime \
    REL_LOG_FORMAT=json

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip \
    && pip install .

RUN mkdir -p /app/runtime/data

EXPOSE 8080

CMD ["python", "rest_api.py"]
