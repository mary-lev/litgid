import json
import django
from django.conf import settings
from datetime import datetime
from django.core.exceptions import MultipleObjectsReturned


settings.configure(DATABASES = {
    'default': {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    'ENGINE': 'django.db.backends.postgresql',
    "NAME": 'd2dduh8uv55mmo',
    "USER": 'eihcelafrqojnn',
    "PASSWORD": 
'c3221b4a66ae8696d7c9cc3e3db08037c60d584ad0d5fa84ae206522288f2b7a',
    "HOST": "ec2-54-228-209-117.eu-west-1.compute.amazonaws.com", 
    "PORT": "5432",
 }
})
django.setup()


from models import Event, Place, Adress, Person


def main():
	with open('c:/Users/anew/litgid/litgid/data/test_1_09_2020.json',
				encoding='utf-8') as f:
		data = json.loads(f.read())
		for line in data['data'][:500]:
			print(line)
			place, created = Place.objects.get_or_create(
				name=line['place'])
			adress, created = Adress.objects.get_or_create(
				name=line['adress'],
				coordinates=line['coordinates'],
				)
			event = Event.objects.create(
				description = line['event'],
				date = datetime.strptime(
					line['date'], '%Y-%m-%d %H:%M:%S'),
				place = place,
				adress = adress,
				)

			event.save()
			for one in set(line['names']):
				try:
					person, created = Person.objects.get_or_create(name=one)
					event.people.add(person)
				except (MultipleObjectsReturned):
					pass


if __name__ == '__main__':
	import django
	django.setup()
	main()
	