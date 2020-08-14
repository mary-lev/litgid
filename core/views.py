from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from rest_framework import viewsets
from django.utils.safestring import mark_safe

import calendar

from .serializers import EventSerializer, PlaceSerializer, AdressSerializer
from .models import Event, Place, Adress
from .utils import EventCalendar


def index(request):
	cards = Event.objects.all()[:3]
	return render(request, 'core/index.html', {'cards': cards})

def new_calendar(request, year, month):
	selected_events = Event.objects.order_by('date').filter(date__year=year, date__month=month)
	c = EventCalendar(selected_events).formatmonth(year, month)
	return render(request, 'core/calendar.html', {'calendar': mark_safe(c)})

def calendar_test(request, year):
	events = Event.objects.filter(date__endswith='2015')
	return render(request, 'core/calendar_test.html', {'events': events})


# Class-based views

class EventDetailView(DetailView):
	model = Event


class PlaceDetailView(DetailView):
	model = Place


class EventListView(ListView):
	paginate_by = 25
	model = Event


class PlaceListView(ListView):
	paginate_by = 25
	model = Place


# CLasses for API

class EventViewSet(viewsets.ModelViewSet):
	queryset = Event.objects.all().order_by('description')
	serializer_class = EventSerializer

class PlaceViewSet(viewsets.ModelViewSet):
	queryset = Place.objects.all()
	serializer_class = PlaceSerializer

class AdressViewSet(viewsets.ModelViewSet):
	queryset = Adress.objects.all()
	serializer_class = AdressSerializer
