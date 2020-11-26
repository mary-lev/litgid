from django.test import TestCase
from django.urls import reverse
from core.models import Person

class TestPerson(TestCase):
    @classmethod
    def setUpTestData(cls):
        Person.objects.create(
            name='Сергей',
            second_name='Елпидифорович',
            family='Сергеев-Ценский')

    def test_set_name(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person.name, 'Сергей')

    def test_get_absolute_url(self):
        person = Person.objects.get(id=1)
        url = person.get_absolute_url()
        self.assertEqual('/person/1/', url)

    def test_show_full_name(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person.show_full_name(), 'Сергей Елпидифорович Сергеев-Ценский')


class TestAdress(TestCase):
    pass
