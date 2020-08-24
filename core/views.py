from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.utils.safestring import mark_safe
from rest_framework import viewsets

import markdown
import os
from litgid.settings import BASE_DIR

from .serializers import EventSerializer, PlaceSerializer, AdressSerializer, PersonSerializer
from .models import Event, Place, Adress, Person
from .utils import EventCalendar, month_name


def index(request):
	cards = Event.objects.all()[:3]
	return render(request, 'core/index.html', {'cards': cards})

def research(request):
	file_path = os.path.join(BASE_DIR, 'Readme.md')
	with open(file_path, encoding='utf-8') as f:
		text = f.read()
	md = markdown.Markdown(extensions=["extra"])
	text = md.convert(text)
	return render(request, 'core/research.html', {'text': mark_safe(text)})

def new_calendar(request, year, month):
	selected_events = Event.objects.order_by('date').filter(date__year=year, date__month=month)
	calendar = EventCalendar(selected_events)
	c = calendar.formatmonth(year, month)
	all_years = range(1998, 2021)

	next_month = calendar.next_month(year, month)
	previous_month = calendar.previous_month(year, month)
	return render(request, 'core/calendar.html', {'calendar': mark_safe(c), 'month': month, \
			'year': year, 'all_years': all_years, \
			'previous': previous_month, 'next': next_month})


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
