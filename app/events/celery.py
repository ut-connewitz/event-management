import os
import celery
import logging
from celery import Celery

#setting up environment variable for using django settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events.settings')

#celery app as entry point for using the tasks
app = Celery('events',
            broker = 'amqp://worker:worker@events_rabbit:5676//',
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
