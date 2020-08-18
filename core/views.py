from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from rest_framework import viewsets
from django.utils.safestring import mark_safe

from .serializers import EventSerializer, PlaceSerializer, AdressSerializer
from .models import Event, Place, Adress
from .utils import EventCalendar, month_name


def index(request):
	cards = Event.objects.all()[:3]
	return render(request, 'core/index.html', {'cards': cards})

def new_calendar(request, year, month):
	selected_events = Event.objects.order_by('date').filter(date__year=year, date__month=month)
	c = EventCalendar(selected_events).formatmonth(year, month)
	all_years = range(1998, 2021)
	previous_month = month - 1
	next_month = month + 1	
	names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
	next_name = names[next_month-1]
	previous_name = names[previous_month-1]
	return render(request, 'core/calendar.html', {'calendar': mark_safe(c), 'month': month, \
			'year': year, 'all_years': all_years, \
			'previous_month': previous_month, 'next_month': next_month, 'next_name': next_name, \
			'previous_name': previous_name})


# Class-based views

class EventDetailView(DetailView):
	model = Event


class PlaceDetailView(DetailView):
	model = Place


class EventListView(ListView):
	paginate_by = 25
	model = Event
	queryset = Event.objects.order_by('date')


class PlaceListView(ListView):
	paginate_by = 25
	model = Place
	queryset = Place.objects.order_by('name')


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
