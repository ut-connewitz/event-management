from django import forms
from django.contrib.auth import password_validation
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

# original django code from https://github.com/django/django/blob/main/django/contrib/auth/forms.py
class SetPasswordMixin:
    """
    Form mixin that validates and sets a password for a user.

    This mixin also support setting an unusable password for a user.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    usable_password_help_text = _(
        "Whether the user will be able to authenticate using a password or not. "
        "If disabled, they may still be able to authenticate using other backends, "
        "such as Single Sign-On or LDAP."
    )

    @staticmethod
    def create_password_fields(label1=_("Password"), label2=_("Password confirmation")):
        password1 = forms.CharField(
            label=label1,
            required=False,
            strip=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            help_text=password_validation.password_validators_help_text_html(),
        )
        password2 = forms.CharField(
            label=label2,
            required=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            strip=False,
            help_text=_("Enter the same password as before, for verification."),
        )
        return password1, password2

    @staticmethod
    def create_usable_password_field(help_text=usable_password_help_text):
        return forms.ChoiceField(
            label=_("Password-based authentication"),
            required=False,
            initial="true",
            choices={"true": _("Enabled"), "false": _("Disabled")},
            widget=forms.RadioSelect(attrs={"class": "radiolist inline"}),
            help_text=help_text,
        )

    def validate_passwords(
        self,
        password1_field_name="password1",
        password2_field_name="password2",
        usable_password_field_name="usable_password",
    ):
        usable_password = (
            self.cleaned_data.pop(usable_password_field_name, None) != "false"
        )
        self.cleaned_data["set_usable_password"] = usable_password
        password1 = self.cleaned_data.get(password1_field_name)
        password2 = self.cleaned_data.get(password2_field_name)

        if not usable_password:
            return self.cleaned_data

        if not password1 and password1_field_name not in self.errors:
            error = ValidationError(
                self.fields[password1_field_name].error_messages["required"],
                code="required",
            )
            self.add_error(password1_field_name, error)

        if not password2 and password2_field_name not in self.errors:
            error = ValidationError(
                self.fields[password2_field_name].error_messages["required"],
                code="required",
            )
            self.add_error(password2_field_name, error)

        if password1 and password2 and password1 != password2:
            error = ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
            self.add_error(password2_field_name, error)

    def validate_password_for_user(self, user, password_field_name="password2"):
        password = self.cleaned_data.get(password_field_name)
        if password and self.cleaned_data["set_usable_password"]:
            try:
                password_validation.validate_password(password, user)
            except ValidationError as error:
                self.add_error(password_field_name, error)

    def set_password_and_save(self, user, password_field_name="password1", commit=True):
        if self.cleaned_data["set_usable_password"]:
            user.set_password(self.cleaned_data[password_field_name])
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user

class CustomAdminPasswordChangeForm(SetPasswordMixin, forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """

    required_css_class = "required"
    usable_password_help_text = SetPasswordMixin.usable_password_help_text + (
        '<ul id="id_unusable_warning" class="messagelist"><li class="warning">'
        "If disabled, the current password for this user will be lost.</li></ul>"
    )
    password1, password2 = SetPasswordMixin.create_password_fields()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["autofocus"] = True
        if self.user.has_usable_password():
            self.fields["usable_password"] = (
                SetPasswordMixin.create_usable_password_field(
                    self.usable_password_help_text
                )
            )

    def clean(self):
        self.validate_passwords()
        self.validate_password_for_user(self.user)
        return super().clean()

    def save(self, commit=True):
        """Save the new password."""
        return self.set_password_and_save(self.user, commit=commit)

    @property
    def changed_data(self):
        data = super().changed_data
        if "set_usable_password" in data or "password1" in data and "password2" in data:
            return ["password"]
        return []
