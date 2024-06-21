from datetime import datetime, timedelta
from django.utils.timezone import get_current_timezone
from backend.models.event import Event
from celery.utils.log import get_task_logger
from .celery import app
from celery import shared_task
import logging

logger = logging.getLogger(__name__)
celery_logger = get_task_logger(__name__) #debug
celery_logger2 = logging.getLogger('celery')


@shared_task
def delete_past_events():
    today = datetime.now(tz=get_current_timezone()).date()
    yesterday = today - timedelta(hours=24)
    # saving the queryset containing the event names and dates to return als result
    past_events=list(Event.objects.filter(date__lte=yesterday))

    #trying to get any logger to work as expected :(
    #logger.info('info celery task deleting: \n'+ str(past_events)) #debug
    #logger.error('error celery task deleting: \n'+ str(past_events)) #debug
    #celery_logger.info('info celery task deleting: \n'+ str(past_events)) #debug
    #celery_logger.error('error celery task deleting: \n'+ str(past_events)) #debug
    celery_logger2.info('info celery task deleting: \n'+ str(past_events)) #debug
    #celery_logger2.error('error celery task deleting: \n'+ str(past_events)) #debug
    #print('print celery task deleting: \n'+ str(past_events))

    #actually deleting the objects in the db
    Event.objects.filter(date__lte=yesterday).delete()

    #return the above variable to show in the results what has been deleted
    return 'deleted past events: ' +str(past_events)



@app.task
def add(x,y):
    return x+y
