from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from backend.models.user import User


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Passwort", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Passwort Bestätigung", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "is_staff", "is_active", "user_permissions"]

    def clean_password2(self):
        # check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwörter stimmen nicht überein")
        return password2

    def save(self, commit=True):
        # save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Passwort"),
        help_text = _(
            "Passwörter werden nicht als Text gespeichert, deswegen ist es nicht möglich"
            "das Passwort dieser Person zu sehen. Es kann jedoch geändert werden unter "
            " <a href=\"../password/\">diesem Link</a>"
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "is_active", "is_superuser", "is_staff", "first_name", "last_name"]

class CustomAdminPasswordChangeForm(AdminPasswordChangeForm):
    password1 = forms.CharField(label="Passwort", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Passwort Bestätigung", widget=forms.PasswordInput)

    class Meta:
        model = User
