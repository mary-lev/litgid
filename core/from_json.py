import json
from datetime import datetime
import django
from django.conf import settings

from django.core.exceptions import MultipleObjectsReturned
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

settings.configure(DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
})
django.setup()


from models import Event, Place, Adress, Person


def main():
	with open('c:/Users/anew/litgid/litgid/data/names_coors.json',
				encoding='utf-8') as f:
		data = json.loads(f.read())
		for line in data['data']:
			if line['index'] > 10816:
				print(line)
				place, created = Place.objects.get_or_create(
					name=line['place'])
				if line['lon']:
					adress, created = Adress.objects.get_or_create(
						lon=line['lon'],
						lat=line['lat'],
						name=line['adress']
						)
				else:
					adress, created = Adress.objects.get_or_create(
						name=line['adress'])
				event = Event.objects.create(
					description = line['event'],
					date = datetime.strptime(
						' '.join([line['day'], line['hour']]), '%d.%m.%Y %H:%M'),
					place = place,
					adress = adress,
					)

				event.save()
				print(type(line['names']))
				for one in line['names']:
					try:
						person, created = Person.objects.get_or_create(
							name=one[0],
							family=one[2])
						event.people.add(person)
					except (MultipleObjectsReturned):
						pass


if __name__ == '__main__':
	import django
	django.setup()
	main()
	