import random
import os
import markdown

from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from rest_framework import viewsets

from litgid.settings import BASE_DIR
from .serializers import EventSerializer, PlaceSerializer
from .serializers import AdressSerializer, PersonSerializer
from .models import Event, Place, Adress, Person
from .utils import FoliumMap
from .forms import PersonForm
from .events_calendar import EventCalendar


def index(request):
	cards = random.sample(list(Event.objects.all()), 3)
	return render(request, 'core/index.html', {'cards': cards})


def research(request):
	file_path = os.path.join(BASE_DIR, 'Readme.md')
	with open(file_path, encoding='utf-8') as file:
		text = file.read()
	markdown_text = markdown.Markdown(extensions=["extra"])
	text = markdown_text.convert(text)
	return render(request, 'core/research.html', {'text': text})


def new_calendar(request, year, month):
	selected_events = Event.objects.order_by('date').filter(
		date__year=year, date__month=month)
	calendar = EventCalendar(selected_events, year, month)
	all_years = range(1998, 2021)
	return render(request, 'core/calendar.html',
		{'calendar': calendar, 'month': month, 'year': year, 'all_years': all_years})


def edit_persons(request, event_id):
	PersonFormSet = modelformset_factory(Person, fields=['name', 'family'])
	event = Event.objects.get(id=event_id)
	if request.method == 'POST':
		myformset = PersonFormSet(request.POST, queryset=Person.objects.filter(event__id=event_id))
		if myformset.is_valid():
			myformset.save()
	else:
		myformset = PersonFormSet(queryset=Person.objects.filter(event__id=event_id))

	return render(request, 'core/edit_persons.html', {'myformset': myformset, 'event': event})


# Class-based views
class EventDetailView(DetailView):
	model = Event


class PlaceDetailView(DetailView):
	model = Place


class PersonDetailView(DetailView):
	model = Person


class EventListView(ListView):
	paginate_by = 25
	model = Event
	context_object_name = 'Список событий'
	queryset = Event.objects.order_by('date')


class PlaceListView(ListView):
	paginate_by = 25
	model = Place
	queryset = Place.objects.order_by('name')


class PersonListView(ListView):
	paginate_by = 25
	model = Person
	queryset = Person.objects.order_by('name')

class PersonUpdate(UpdateView):
	model = Person
	fields = ['name', 'second_name', 'family']
	success_url = reverse_lazy('core:persons')


class PersonDelete(DeleteView):
	model = Person
	success_url = reverse_lazy("core:persons")


class EventUpdate(UpdateView):
	model = Event
	fields = ['description', 'people']
	success_url = reverse_lazy('core:events')
	


class FoliumView(TemplateView):
	template_name = 'core/map.html'

	def get_context_data(self, **kwargs):
		queryset = Adress.objects.all().distinct()
		events_map = FoliumMap(queryset).create_folium_map()
		return {'map': events_map}


# CLasses for API
class EventViewSet(viewsets.ModelViewSet):
	queryset = Event.objects.all()
	serializer_class = EventSerializer


class PlaceViewSet(viewsets.ModelViewSet):
	queryset = Place.objects.all()
	serializer_class = PlaceSerializer


class AdressViewSet(viewsets.ModelViewSet):
	queryset = Adress.objects.all()
	serializer_class = AdressSerializer


class PersonViewSet(viewsets.ModelViewSet):
	queryset = Person.objects.all()
	serializer_class = PersonSerializer
