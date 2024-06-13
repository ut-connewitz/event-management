from datetime import datetime, timedelta
from django.utils.timezone import get_current_timezone
from backend.models.event import EventDay
from celery.utils.log import get_task_logger
from .celery import app
import logging

logger = logging.getLogger(__name__)
celery_logger = get_task_logger(__name__) #debug
celery_logger2 = logging.getLogger('celery')


@app.task(ignore_result = True)
def delete_past_eventdays():
    today = datetime.now(tz=get_current_timezone()).date()
    yesterday = today - timedelta(hours=24)
    past_eventdays=EventDay.objects.filter(date__lte=yesterday)

    logger = logging.getLogger(__name__)
    celery_logger = get_task_logger(__name__) #debug
    celery_logger2 = logging.getLogger('celery')


    logger.info('info celery task deleting: \n'+ str(past_eventdays)) #debug
    logger.error('error celery task deleting: \n'+ str(past_eventdays)) #debug
    celery_logger.info('info celery task deleting: \n'+ str(past_eventdays)) #debug
    celery_logger.error('error celery task deleting: \n'+ str(past_eventdays)) #debug
    celery_logger2.info('info celery task deleting: \n'+ str(past_eventdays)) #debug
    celery_logger2.error('error celery task deleting: \n'+ str(past_eventdays)) #debug
    print('print celery task deleting: \n'+ str(past_eventdays))

    return 'test return'



@app.task
def add(x,y):
    return x+y
