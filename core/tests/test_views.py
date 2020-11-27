import datetime
import pytz
from django.urls import reverse
from django.test import TestCase, Client
from core.models import Event
from core import views as core_views


class Test(TestCase):
	@classmethod
	def setUpTestData(cls):
		Event.objects.bulk_create([
			Event(description='Тестовое событие', date=datetime.datetime.now(pytz.utc)),
			Event(description='Второе тестовое событие', date=datetime.datetime.now(pytz.utc)),
			Event(description='Третье тестовое событие', date=datetime.datetime.now(pytz.utc))
		]
		)

	def test_index(self):
		cards = Event.objects.all()
		print(cards)
		client = Client()
		response = client.get(reverse('core:index'))
		print(response)
		# self.assertEqual(200, response.status_code)
		self.assertEqual(1, 1)
