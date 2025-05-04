FROM python:3.12.6-slim-bookworm  AS builder

WORKDIR /app

COPY requirements/requirements.txt requirements/requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements-test.txt

COPY . .

RUN python manage.py migrate --noinput && pytest tests/

FROM python:3.12.6-slim-bookworm 

WORKDIR /app

COPY requirements/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]