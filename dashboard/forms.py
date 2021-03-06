from django import forms
# from django.core import validators


def must_be_empty(value):
    if value:
        print('must be eumpty')
        raise forms.ValidationError('is not empty')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField(max_length=120)
    phone = forms.CharField(max_length=15, required=False)
    message = forms.CharField(widget=forms.Textarea)
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label='Leave empty!', validators=[
                            # validators.MaxLengthValidator(0)
                            must_be_empty,
                            ])
'''
    def clean(self):

        honeypot = self.cleaned_data['honeypot']
        if len(honeypot):
            print('clear')
            raise forms.ValidationError('Honey pot must be empty. Bad bot!')
        super().clean()

'''

# From Kenneth Love's Class Based Views -- crash course youtube tutorial

# https://www.youtube.com/watch?v=KZHXjGP71kQ&list=PLTOBJKrkhpoOO7enfsbFQI-oV6KStqvye
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit


class RegistrationForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username', 'password1', 'password2',
            ButtonHolder(
                Submit('register', 'Register', css_class='btn btn-primary')
            )
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username', 'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn btn-primary')
            )
        )
