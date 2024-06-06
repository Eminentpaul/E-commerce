from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Enter Password",
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Confirm Password"
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
            self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
            self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
