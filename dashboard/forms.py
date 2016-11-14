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