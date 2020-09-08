import random
import os
import markdown

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView

from rest_framework import viewsets
from django_super_deduper.merge import MergedModelInstance

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
                  {'calendar': calendar, 'month': month, 'year': year, 'all_years': all_years})


def edit_persons(request, event_id):
    PersonFormSet = modelformset_factory(
        Person,
        fields=['name', 'second_name', 'family'],
        can_delete=True)
    event = Event.objects.get(id=event_id)
    #NewPersonFormSet = modelformset_factory(
    #    Person,
    #    fields=['name', 'second_name', 'family'])
    if request.method == 'POST':
        myformset = PersonFormSet(request.POST, queryset=Person.objects.filter(event__id=event_id))
    #    my_new_formset = NewPersonFormSet(request.POST)
        if myformset.is_valid():
            myformset.save()
            return redirect('core:one_event', pk=event_id)
#        if my_new_formset.is_valid():
#            new_person = my_new_formset.save(commit=False)
#            event.people.add(new_person)
#            new_person.save_m2m()
#            return redirect('core:one_event', pk=event_id)
    else:
        myformset = PersonFormSet(queryset=Person.objects.filter(event__id=event_id))
    #    my_new_formset = NewPersonFormSet()

    return render(request, 'core/edit_persons.html', {
        'myformset': myformset, 
        #'my_new_formset': my_new_formset, 
        'event': event})


def update_event_with_person(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            #if Person.objects.filter(name=person['name'], family=person['family']).exists():
            #    messages.error(request, 'person already exists')
                #event.people.add(Person.objects.get(name=person['name'], family=person['family']))
                #return redirect('core:one_event', pk=event_id)
            event.people.add(person)
            person.save()
            return redirect('core:one_event', pk=event_id)
        else:
            person = form.cleaned_data
            add_person = Person.objects.get(name=person['name'], family=person['family'])
            event.people.add(add_person)
            return redirect('core:one_event', pk=event_id)
    else:
        form = PersonForm()
    return render(request, 'core/person_add.html', {'form': form, 'event_id': event_id})


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
    queryset = Person.objects.order_by('family')


class PersonUpdate(UpdateView):
    model = Person
    fields = ['name', 'second_name', 'family']

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
