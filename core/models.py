from django.db import models
from django.urls import reverse
from django.db.models import Count

class Person(models.Model):
	name = models.CharField(max_length=300)
	second_name = models.CharField(max_length=300)
	family = models.CharField(max_length=300)

	class Meta:
		verbose_name = "Person"
		app_label = 'core'

	def __str__(self):
		return self.name


class Adress(models.Model):
	name = models.CharField(max_length=300)
	coordinates = models.CharField(max_length=300, blank=True, null=True)

	class Meta:
		app_label = 'core'
		verbose_name = 'Adress'

	def __str__(self):
		return self.name


class Place(models.Model):
	name = models.CharField(max_length=300)

	class Meta:
		app_label = 'core'
		verbose_name = 'Place'

	def __str__(self):
		return self.name

	def get_adresses(self):
		events = Event.objects.filter(place=self).values_list('adress',\
										 flat=True).order_by('id')
		adresses = Adress.objects.filter(id__in=events)
		return adresses


class Event(models.Model):
	description = models.TextField()
	date = models.DateTimeField(auto_now=False, auto_now_add=False)
	place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)
	adress = models.ForeignKey(Adress, on_delete=models.CASCADE, blank=True, null=True)
	people = models.ManyToManyField(Person, blank=True)

	class Meta:
		app_label = 'core'
		verbose_name = 'Event'
		ordering = ['date']

	def __str__(self):
		return self.description

	def get_absolute_url(self):
		return reverse('core:one_event', args=[self.id])



