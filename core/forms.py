from django import forms
from crispy_forms.helper import FormHelper
from .models import Event, Place, Adress, Person


class PersonEventForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=20)
    second_name = forms.CharField(label='Отчество', max_length=20)
    family = forms.CharField(label='Фамилия', max_length=20)

