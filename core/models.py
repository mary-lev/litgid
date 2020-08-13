from django.db import models

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


class Event(models.Model):
	description = models.TextField()
	date = models.CharField(max_length=300, blank=True, null=True)
	place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)
	adress = models.ForeignKey(Adress, on_delete=models.CASCADE, blank=True, null=True)
	people = models.ManyToManyField(Person, blank=True)

	class Meta:
		app_label = 'core'
		verbose_name = 'Event'

	def __str__(self):
		return self.description



