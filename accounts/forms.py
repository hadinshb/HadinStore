from .models import Account
from django.forms import ModelForm


class RegistrationForm(ModelForm):
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number','email','password']


