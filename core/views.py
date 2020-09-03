from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from rest_framework import viewsets

import random
import os
import markdown

from litgid.settings import BASE_DIR
from .serializers import EventSerializer, PlaceSerializer,\
						AdressSerializer, PersonSerializer
from .models import Event, Place, Adress, Person

from .utils import FoliumMap
from .events_calendar import EventCalendar


def index(request):
	cards = random.sample(list(Event.objects.all()), 3)
	return render(request, 'core/index.html', {'cards': cards})


def research(request):
	file_path = os.path.join(BASE_DIR, 'Readme.md')
	with open(file_path, encoding='utf-8') as f:
		text = f.read()
	md = markdown.Markdown(extensions=["extra"])
	text = md.convert(text)
	return render(request, 'core/research.html', {'text': text})


def new_calendar(request, year, month):
	selected_events = Event.objects.order_by('date').filter(
		date__year=year, date__month=month)
	calendar = EventCalendar(selected_events, year, month)
	all_years = range(1998, 2021)
	return render(request, 'core/calendar.html',
		{'calendar': calendar, 'month': month, 'year': year, 'all_years': all_years})


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
	fields = '__all__'


class PersonDelete(DeleteView):
	model = Person
	success_url = reverse_lazy("core:persons")


class EventUpdate(UpdateView):
	model = Event
	fields = "__all__"


class FoliumView(TemplateView):
	template_name = 'core/map.html'

	def get_context_data(self, **kwargs):
		queryset = Adress.objects.all().distinct()
		m = FoliumMap(queryset).create_folium_map()
		return {'map': m}


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
