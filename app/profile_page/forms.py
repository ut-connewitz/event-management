from django.forms import ModelForm
from backend.models.user import User

class AccountForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
