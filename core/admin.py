from django.contrib import admin

from .models import Person, Place, Adress, Event

admin.site.register(Person)
admin.site.register(Place)
admin.site.register(Adress)
admin.site.register(Event)
