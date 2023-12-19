from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CheckboxSelectMultiple, ModelMultipleChoiceField

from .models import Driver, Car


def validate_license_number(license_number: str) -> str:
    if len(license_number) != 8:
        raise ValidationError("License number must consist of 8 characters")
    if not (license_number[:3].isupper() and license_number[3:].isdigit()):
        raise ValidationError("First 3 characters must be uppercase letters and last 5 characters must be digits")
    return license_number


class DriverCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data.get("license_number")
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data.get("license_number")
        return validate_license_number(license_number)


class CarForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"