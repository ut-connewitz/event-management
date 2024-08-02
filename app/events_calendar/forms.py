from django.forms import ModelForm, DateInput, TimeInput, BooleanField, HiddenInput, DateField
from backend.models.event import Event, PastEvent
from backend.models.task import Task, Volunteering
from datetime import datetime

import logging

class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {
            'date': DateInput(
                format=('%d.%m.%Y'),
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Datum wählen',
                    #'type': 'date',
                    # chosing the 'type': 'date' option enables the actual date-picking widget
                    # but defaults the input value to the current date and makes saving dates impossible
                    # due to a format error
                    }),
            'start_time': TimeInput(
                format=('%H:%M'),
                attrs={
                    'type': 'time-local',
                    'class': 'form-control'}),
            'admission_time': TimeInput(
                format=('%H:%M'),
                attrs={
                'type': 'time-local',
                'class': 'form-control'}),
            'duration': TimeInput(
                format=('%H:%M'),
                attrs={
                    'class': 'form-control'}),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%H:%M',)
        self.fields['admission_time'].input_formats = ('%H:%M',)
        self.fields['duration'].input_formats = ('%H:%M',)
        #self.fields['duration'].help_text = 'Eingabeformat der Veranstaltungsdauer: HH:MM'
        self.fields['date'].input_formats = ('%d.%m.%Y',)
        #logger = logging.getLogger(__name__) #debug
        #logger.error(str(self.instance.date)) #debug
        #logger.error(str(self.instance.date.strftime('%d.%m.%Y')))
        #self.fields['date'].initial = self.instance.date.strftime('%d.%m.%Y')
        #self.fields['date'].initial = self.instance.date

class PastEventForm(ModelForm):
    class Meta:
        model = PastEvent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PastEventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%H:%M',)
        self.fields['date'].input_formats = ('%d.%m.%Y',)
        #logger = logging.getLogger(__name__) #debug
        #logger.error(str(self.instance.date)) #debug
        #logger.error(str(self.instance.date.strftime('%d.%m.%Y')))
        #self.fields['date'].initial = self.instance.date.strftime('%d.%m.%Y')

class TaskForm(ModelForm):
    # this hidden fields purpose is determine which form is submitted in the post request
    # it is needed because there are two different forms (TaskForm and VolunteeringForm) on one page
    edit_task = BooleanField(widget=HiddenInput, initial=True)

    class Meta:
        model = Task
        widgets = {
            'start_time': TimeInput(
                format=('%H:%M'),
                attrs={
                    'type': 'time-local',
                    'class': 'form-control'}),
            'finish_time': TimeInput(
                format=('%H:%M'),
                attrs={
                    'type': 'time-local',
                    'class': 'form-control'}),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%H:%M',)
        self.fields['finish_time'].input_formats = ('%H:%M',)

        #if request.user.is_staff == False:
        #    self.fields['event_day', 'task_type', 'team_restriction', 'urgency', 'state', 'start_time', 'finish_time', 'comment'].disabled = True


class VolunteeringForm(ModelForm):
    edit_volunteering = BooleanField(widget=HiddenInput, initial=True)

    class Meta:
        model = Volunteering
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VolunteeringForm, self).__init__(*args, **kwargs)
