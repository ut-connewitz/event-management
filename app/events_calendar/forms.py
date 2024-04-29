from django.forms import ModelForm, DateInput
from backend.models.event import EventDay
from backend.models.task import Task

class EventDayForm(ModelForm):
    class Meta:
        model = EventDay
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'admission_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventDayForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['admission_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class TaskForm(ModelForm):
    class Meta:
        model = Task
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'finish_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['finish_time'].input_formats = ('%Y-%m-%dT%H:%M',)

        #if request.user.is_staff == False:
        #    self.fields['event_day', 'task_type', 'team_restriction', 'urgency', 'state', 'start_time', 'finish_time', 'comment'].disabled = True
