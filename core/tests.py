from django.test import TestCase
from .models import Person


class PersonTestCase(TestCase):
    def setUp(self):
        Person.objects.create(
            name='Иван',
            second_name='Иванович',
            family='Иванов')
        Person.objects.create(
            name='Сергей',
            family='Сергеев-Ценский Второй')
        Person.objects.create(
            name='Елпидифор',
            family='Львов-Курачевский')

    def test_person_has_name(self):
        """Не знаю что мы тестируем."""
        person_one = Person.objects.get(family='Сергеев-Ценский Второй')
        person_two = Person.objects.get(family='Львов-Курачевский')
        self.assertEqual(person_one.name, 'Сергей')
        self.assertEqual(person_two.name, 'Елпидифор')

    def test_person_has_family(self):
        person_one = Person.objects.get(name='Елпидифор')
        self.assertEqual(person_one.family, 'Львов-Курачевский')
