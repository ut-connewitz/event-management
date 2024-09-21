import os
import celery
import logging
from celery import Celery
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#setting up environment variable for using django settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events.settings')

rabbit_worker = os.environ.get('RABBITMQ_WORKER')
rabbit_worker_pass = os.environ.get('RABBITMQ_WORKER_PASS')

#celery app as entry point for using the tasks
app = Celery('events',
            broker = f'amqp://{rabbit_worker}:{rabbit_worker_pass}@events_rabbit:5672//',
            #backend = 'amqp://worker:worker@events_rabbit:5676//',
            include = ['events.celery_tasks', ]
            )

#using django settings file to configure app
app.config_from_object('django.conf:settings', namespace='CELERY')

#load all task modules from registered django apps
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.reguest!r}')

@celery.signals.after_setup_logger.connect
def on_after_setup_logger(**kwargs):
    logger = logging.getLogger('celery')
    logger.propagate = True
    logger = logging.getLogger('celery.app.trace')
    logger.propagate = True

if __name__ == '__main__':
    app.start()
