from django.db import models
from django.urls import reverse


class Person(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True,
                            verbose_name='Имя')
    second_name = models.CharField(max_length=300, blank=True, null=True,
                                   verbose_name='Отчество')
    family = models.CharField(max_length=300, blank=True, null=True,
                              verbose_name='Фамилия')
    pseudonym = models.CharField(max_length=100, blank=True,
                                 verbose_name='Псевдоним')

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"
        app_label = 'core'
        unique_together = (('name', 'family'),)
        ordering = ['family', 'name']

    def __str__(self):
        """Save from None in self.name."""
        return f'{self.name} {self.second_name} {self.family}'

    def get_absolute_url(self):
        return reverse('core:one_person', args=[self.id])

    def show_full_name(self):
        if self.name:
            first_name = self.name
        else:
            first_name = ''
        if self.second_name:
            second_name = self.second_name
        else:
            second_name = ''
        if self.family:
            family = self.family
        else:
            family = ''

        return '{0} {1} {2}'.format(first_name, second_name, family)


class Adress(models.Model):
    name = models.CharField(max_length=300)
    lon = models.DecimalField(
        max_digits=10, decimal_places=8, blank=True, null=True)
    lat = models.DecimalField(
        max_digits=10, decimal_places=8, blank=True, null=True)

    class Meta:
        app_label = 'core'
        verbose_name = 'Адрес'
        verbose_name_plural = "Адреса"

    def __str__(self):
        return f'{self.name}'


class Place(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        app_label = 'core'
        verbose_name = 'Место'
        verbose_name_plural = "Места"

    def __str__(self):
        return f'{self.name}'

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
        verbose_name = 'Событие'
        verbose_name_plural = "События"
        ordering = ['date']

    def __str__(self):
        return f'{self.description}'

    def get_absolute_url(self):
        return reverse('core:one_event', args=[self.id])
