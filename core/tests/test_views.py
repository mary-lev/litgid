import os
import datetime
import pytz
from django.urls import reverse
from django.test import TestCase, Client
from litgid.settings import BASE_DIR
from core.models import Event
from core import views as core_views


class TestIndex(TestCase):
	@classmethod
	def setUpTestData(cls):
		Event.objects.bulk_create([
			Event(description='Тестовое событие', date=datetime.datetime.now(pytz.utc)),
			Event(description='Второе тестовое событие', date=datetime.datetime.now(pytz.utc)),
			Event(description='Третье тестовое событие', date=datetime.datetime.now(pytz.utc))
		]
		)

	def test_index_page(self):
		cards = Event.objects.all()
		client = Client()
		response = client.get(reverse('core:index'))
		self.assertEqual(200, response.status_code)
		self.assertEqual(core_views.index, response.resolver_match.func)
		self.assertEqual(len(response.context['cards']), 3)
		self.assertTemplateUsed(response, template_name='core/index.html')
		self.assertContains(response, 'СПбЛитГид: 1999—2019')


class TestResearch(TestCase):
	def test_readme_file(self):
		client = Client()
		file_path = os.path.join(BASE_DIR, 'Readme.md')
		with open(file_path, 'r', encoding='utf-8') as f:
			text = f.read()
		response = client.get(reverse('core:research'))
		self.assertIsNotNone(file_path)
		self.assertIsNotNone(text)
		self.assertTemplateUsed(response, template_name='core/research.html')
		self.assertEqual(response.status_code, 200)
