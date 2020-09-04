from django import forms
from crispy_forms.helper import FormHelper
from .models import Event, Place, Adress, Person


class PersonEditForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'



