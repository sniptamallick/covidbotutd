from django import forms

class NameForm(forms.Form):
    message = forms.CharField(label='message', max_length= 1000)