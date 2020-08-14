from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from rest_framework import viewsets

import calendar

from .serializers import EventSerializer, PlaceSerializer, AdressSerializer
from .models import Event, Place, Adress

def index(request):
	cards = Event.objects.all()[:3]
	return render(request, 'core/index.html', {'cards': cards})

def new_calendar(request):
	c = calendar.HTMLCalendar(calendar.SUNDAY)
	s = c.formatmonth(2020, 1)
	return render(request, 'core/calendar.html', {'calendar': s})


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
