from django.test import TestCase
from core.models import Person, Adress, Place, Event
import datetime
import pytz

class TestPerson(TestCase):
    """Тесты для модели Person."""

    @classmethod
    def setUpTestData(cls):
        Person.objects.create(
            name='Сергей',
            second_name='Елпидифорович',
            family='Сергеев-Ценский')

    def test_set_name(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person.name, 'Сергей')
        self.assertEqual(person.pseudonym, '')

    def test_str(self):
        person = Person.objects.get(id=1)
        self.assertEqual(str(person), "{0} {1} {2}".format(person.name, person.second_name, person.family))

    def test_get_absolute_url(self):
        person = Person.objects.get(id=1)
        url = person.get_absolute_url()
        self.assertEqual('/person/1/', url)

    def test_show_full_name(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person.show_full_name(), 'Сергей Елпидифорович Сергеев-Ценский')


class TestAdress(TestCase):
    """Тесты для модели Address."""

    @classmethod
    def setUpTestData(cls):
        Adress.objects.create(name='ул. Октябрьская, д. 31')

    def test_set_name(self):
        address = Adress.objects.get(id=1)
        self.assertEqual(address.name, 'ул. Октябрьская, д. 31')
        self.assertEqual(address.lat, None)

    def test_str(self):
        address = Adress.objects.get(id=1)
        self.assertEqual(address.name, str(address))


class TestPlace(TestCase):
    """Тесты для модели Place."""

    @classmethod
    def setUpTestData(cls):
        place = Place.objects.create(name='Эрарта')
        address = Adress.objects.create(name='Новая наб., д. 10')
        person = Person.objects.create(name='Иван', family='Умнов')
        event = Event.objects.create(
            description='Презентация книги',
            date=datetime.datetime.now(pytz.utc),
            place=place,
            adress=address
            )
        event.people.add(person)

    def test_str(self):
        place = Place.objects.get(id=1)
        self.assertEqual(place.name, str(place))

    def test_show_adresses(self):
        event = Event.objects.get(id=1)
        address = Adress.objects.get(id=1)
        self.assertEqual(event.adress, address)

class TestEvent(object):
    """Тесты для модели Event."""
    
    def setUpTestData(cls):
        pass

    def test_str(self):
        event = Event.objects.get(id=1)
        self.assertEqual(event.description, str(event))
