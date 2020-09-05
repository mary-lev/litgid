from django.forms import BaseFormSet
from crispy_forms.helper import FormHelper
from .models import Event, Place, Adress, Person


class PersonForm(BaseFormSet):

    class Meta:
        model = Person
        fields = '__all__'



