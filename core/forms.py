from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from .models import Event, Place, Adress, Person

class PersonUpdate(UpdateView):
	model = Person
	fields = '__all__'


class PersonDelete(DeleteView):
	model = Person
	success_url = reverse_lazy("core:persons")


class EventUpdate(UpdateView):
	model = Event
	fields = "__all__"