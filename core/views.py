import random
import os
import markdown

from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

from rest_framework import viewsets

from litgid.settings import BASE_DIR
from .serializers import EventSerializer, PlaceSerializer
from .serializers import AdressSerializer, PersonSerializer
from .models import Event, Place, Adress, Person
from .utils import FoliumMap
from .forms import PersonForm
from .events_calendar import EventCalendar


def custom_handler404(request, exception):
    return render(request, '404.html', status=404)


def custom_handler500(request):
    return render(request, '404.html', status=500)


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
                  {'calendar': calendar,
                  'month': month,
                  'year': year,
                  'all_years': all_years})


def edit_persons(request, event_id):
    PersonFormSet = modelformset_factory(
        Person,
        fields=['name', 'second_name', 'family', 'pseudonym'],
        can_delete=True)
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        myformset = PersonFormSet(request.POST,
                                    queryset=Person.objects.filter(event__id=event_id))
        if myformset.is_valid():
            myformset.save()
            return redirect('core:one_event', pk=event_id)
    else:
        myformset = PersonFormSet(
            queryset=Person.objects.filter(event__id=event_id))

    return render(request, 'core/edit_persons.html', {
        'myformset': myformset,
        'event': event})


def update_event_with_person(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            event.people.add(person)
        else:
            person = form.cleaned_data
            add_person = Person.objects.get(
                name=person['name'],
                family=person['family'])
            event.people.add(add_person)
        return redirect('core:one_event', pk=event_id)
    else:
        form = PersonForm()
    return render(request, 'core/person_add.html', {
        'form': form, 
        'event_id': event_id})


# Class-based views
class EventCreateView(CreateView):
    model = Event
    fields = "__all__"


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
    queryset = Person.objects.all().annotate(events=Count('event')).order_by('-events')


class PersonSearch(PersonListView):
    def get_queryset(self):
        query = self.request.GET.get('search', '')
        return Person.objects.filter(
            Q(family__icontains=query) | Q(name__icontains=query))


class NormalPersonListView(ListView):
    model = Person
    paginate_by = 25
    queryset = Person.objects.all().order_by('family', 'name')

class PersonUpdate(UpdateView):
    model = Person
    fields = ['name', 'second_name', 'family', 'pseudonym']

    def form_invalid(self, form):
        events = Event.objects.filter(people__id=self.object.id).all()
        person_for_add = Person.objects.get(name=form.cleaned_data['name'],
                family=form.cleaned_data['family'])
        person_for_delete = Person.objects.get(id=self.object.id)
        for event in events:
            event.people.add(person_for_add)
            event.people.remove(person_for_delete)
        return redirect('core:one_person', pk=self.object.id)

    def get_success_url(self):
        return reverse_lazy('core:one_person', args=([self.object.id]))


class PersonDelete(DeleteView):
    model = Person
    success_url = reverse_lazy("core:persons")


class EventUpdate(UpdateView):
    model = Event
    fields = ['description', 'people']

    def get_success_url(self):
        return reverse_lazy('core:one_event', args=([self.object.id]))


class FoliumView(TemplateView):
    template_name = 'core/map.html'

    def get_context_data(self, **kwargs):
        queryset = Adress.objects.filter(lat__isnull=False).values(
            'event__place__name',
            'event__place__id',
            'lat',
            'lon').distinct()
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
