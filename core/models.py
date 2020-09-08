from django.db import models
from django.urls import reverse


class Person(models.Model):
	name = models.CharField(max_length=300, blank=True, null=True, verbose_name='Имя')
	second_name = models.CharField(max_length=300, blank=True, null=True, verbose_name='Отчество')
	family = models.CharField(max_length=300, blank=True, null=True, verbose_name='Фамилия')

	class Meta:
		verbose_name = "Person"
		app_label = 'core'
		unique_together = (('name', 'family'),)
		ordering = ['family', 'name']

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('core:one_person', args=[self.id])

	def show_full_name(self):
		if self.second_name:
			second_name = self.second_name
		else:
			second_name = ''

		return '{0} {1} {2}'.format(
			self.name,
			second_name,
			self.family)


class Adress(models.Model):
	name = models.CharField(max_length=300)
	lon = models.DecimalField(
		max_digits=10, decimal_places=8, blank=True, null=True)
	lat = models.DecimalField(
		max_digits=10, decimal_places=8, blank=True, null=True)

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

	def show_adresses(self):
		events = Event.objects.filter(place=self).values_list(
			'adress', flat=True).order_by('id')
		adresses = Adress.objects.filter(id__in=events)
		return adresses


class Event(models.Model):
	description = models.TextField()
	date = models.DateTimeField(auto_now=False, auto_now_add=False)
	place = models.ForeignKey(
		Place, on_delete=models.CASCADE, blank=True, null=True)
	adress = models.ForeignKey(
		Adress, on_delete=models.CASCADE, blank=True, null=True)
	people = models.ManyToManyField(Person, related_name='event', blank=True)

	class Meta:
		app_label = 'core'
		verbose_name = 'Event'
		ordering = ['date']

	def __str__(self):
		return self.description

	def get_absolute_url(self):
		return reverse('core:one_event', args=[self.id])
