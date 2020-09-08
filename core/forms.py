from django import forms
from .models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'second_name', 'family', 'pseudonym']


class PersonEventForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=20)
    second_name = forms.CharField(label='Отчество', max_length=20)
    family = forms.CharField(label='Фамилия', max_length=20)
