from django.forms import ModelForm, DateInput, TimeInput, BooleanField, HiddenInput
from backend.models.event import EventDay
from backend.models.task import Task, Volunteering

class EventDayForm(ModelForm):
    class Meta:
        model = EventDay
        widgets = {
            'date': DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                    'placeholder': 'Datum wählen',
                    'type': 'date',
                    }),
            'start_time': TimeInput(format=('%H:%M'), attrs={'type': 'time', 'class': 'timepicker'}),
            'admission_time': TimeInput(format=('%H:%M'), attrs={'type': 'time', 'class': 'timepicker'}),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventDayForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%H:%M',)
        self.fields['admission_time'].input_formats = ('%H:%M',)

class TaskForm(ModelForm):
    # this hidden fields purpose is determine which form is submitted in the post request
    # it is needed because there are two different forms (TaskForm and VolunteeringForm) on one page
    edit_task = BooleanField(widget=HiddenInput, initial=True)

    class Meta:
        model = Task
        widgets = {
            'start_time': TimeInput(format=('%H:%M'), attrs={'type': 'time', 'class': 'timepicker'}),
            'finish_time': TimeInput(format=('%H:%M'), attrs={'type': 'time', 'class': 'timepicker'}),
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
