import requests
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
    viaf_id = models.CharField(max_length=50, blank=True, null=True,
                               verbose_name='VIAF ID')
    viaf_name = models.CharField(max_length=300, blank=True, null=True,
                                    verbose_name='VIAF Name')
    viaf_id_alternative = models.CharField(max_length=50, blank=True, null=True,
                                          verbose_name='VIAF ID')
    wikidata_id = models.CharField(max_length=50, blank=True, null=True,
                                   verbose_name='Wikidata ID')
    transliterated_name = models.CharField(max_length=300, blank=True, null=True,
                                            verbose_name='Транслитерированное имя')

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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     person = self.object

    #     # Fetch VIAF data if the VIAF ID exists
    #     if person.viaf_id:
    #         viaf_data = self.fetch_viaf_data(person.viaf_id)
    #         context['viaf_data'] = viaf_data

    #     # Fetch Wikidata data if the Wikidata ID exists
    #     if person.wikidata_id:
    #         wikidata_data = self.fetch_wikidata_data(person.wikidata_id)
    #         context['wikidata_data'] = wikidata_data

    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viaf_data'] = {"test_key": "test_value"}  # Hardcoded test data
        context['wikidata_data'] = {"test_key": "test_value"}  # Hardcoded test data
        return context

    def fetch_viaf_data(self, viaf_id):
        url = f'https://viaf.org/viaf/{viaf_id}/viaf.json'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching VIAF data: {e}")
            return None

    def fetch_wikidata_data(self, wikidata_id):
        url = f'https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Wikidata data: {e}")
            return None


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
