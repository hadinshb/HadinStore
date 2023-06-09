from .models import Account
from django import forms


class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    password_confirm=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number','email','password','password_confirm']

    def __init__(self,*arg,**karg):
        super(RegistrationForm,self).__init__(*arg,**karg)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')
        password_confrim=cleaned_data.get('password_confirm')
        if password != password_confrim:
            raise forms.ValidationError('Passwords does not match!')