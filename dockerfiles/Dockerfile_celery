FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY app /app/

RUN mkdir -p /scripts
COPY ./scripts/ /scripts
RUN chmod +x /scripts/celery.sh

CMD ["/scripts/celery.sh"]
