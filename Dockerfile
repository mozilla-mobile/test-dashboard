FROM python:3.9-slim

ENV PYTHONUNBUFFERED True

RUN set -ex \
  && apt-get update && apt-get install -y --no-install-recommends \
    wget

ENV PORT 8080

COPY . /app
WORKDIR /app

RUN set -ex; \
    pip install -r requirements.txt

CMD gunicorn -b 0.0.0.0:${PORT} --workers 1 --threads 8 --timeout 0 main:app
