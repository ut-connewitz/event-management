from django.forms import ModelForm, DateInput, BooleanField, HiddenInput
from backend.models.event import EventDay
from backend.models.task import Task, Volunteering

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
    # this hidden fields purpose is determine which form is submitted in the post request
    # it is needed because there are two different forms (TaskForm and VolunteeringForm) on one page
    edit_task = BooleanField(widget=HiddenInput, initial=True)

    class Meta:
        model = Task
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'finish_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['finish_time'].input_formats = ('%Y-%m-%dT%H:%M',)

        #if request.user.is_staff == False:
        #    self.fields['event_day', 'task_type', 'team_restriction', 'urgency', 'state', 'start_time', 'finish_time', 'comment'].disabled = True


class VolunteeringForm(ModelForm):
    edit_volunteering = BooleanField(widget=HiddenInput, initial=True)

    class Meta:
        model = Volunteering
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VolunteeringForm, self).__init__(*args, **kwargs)
