from datetime import datetime, timedelta
from django.utils.timezone import get_current_timezone

from celery.utils.log import get_task_logger
from .celery import app
from celery import shared_task

from backend.models.event import Event, PastEvent

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

    for event in past_events:
        past_event = PastEvent.objects.create(
            past_event_id = event.event_id,
            series = event.series,
            date = event.date,
            start_time = event.start_time,
            duration = event.duration,
            comment = event.comment,
        )
        past_event.save()

        # having one event_act class have a fk the two event classes does not work nativeley in this case
        # because:
        # 1. abstract base classes cant be used as fk class.
        # 2. multi table inheritance leaves original model field values in the inherited table, which is intended to be deleted here.
        # 3. proxy models are located in the same db table and reversely accesable, which contradicts the purpose of the event model separation.
        # 4. PolymorphicModel from django-polymorphic does not support Django >4.0 and would add another external dependency.
        # https://docs.djangoproject.com/en/4.2/db/models/#model-inheritance
        # httpy://django-polymorphic.readthedocs.io/en/latest/index.html
        # if needed maybe give event_act two fk fields or
        # maybe also archive the event_act like this
        #try:
        #    event_act = EventAct.objects.get(event=event)
        #    past_event_act = PastEventAct.objects.create(...)
        #    past_event_act.save()
        #except EventAct.DoesNotExist:
        #    pass



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
