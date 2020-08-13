from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import viewsets

from .serializers import EventSerializer, PlaceSerializer, AdressSerializer
from .models import Event, Place, Adress

def index(request):
	cards = Event.objects.all()[:3]
	return render(request, 'core/index.html', {'cards': cards})

class EventListView(ListView):
	model = Event


class EventViewSet(viewsets.ModelViewSet):
	queryset = Event.objects.all().order_by('description')
	serializer_class = EventSerializer

class PlaceViewSet(viewsets.ModelViewSet):
	queryset = Place.objects.all()
	serializer_class = PlaceSerializer

class AdressViewSet(viewsets.ModelViewSet):
	queryset = Adress.objects.all()
	serializer_class = AdressSerializer
