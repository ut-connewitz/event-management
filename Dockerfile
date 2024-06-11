FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY app /app/

WORKDIR /app
COPY ./scripts /scripts
RUN chmod +x /scripts/*

RUN adduser -disabled-login user
USER user

USER root

RUN chown -R root /scripts
RUN chgrp root /scripts
RUN chmod -R 755 /scripts


CMD ["scripts/celery.sh"]
