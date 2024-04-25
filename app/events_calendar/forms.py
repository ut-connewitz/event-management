from django.forms import ModelForm, DateInput
from backend.models.event import EventDay

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
