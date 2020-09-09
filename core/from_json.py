import json
from datetime import datetime
import django
from django.conf import settings

from django.core.exceptions import MultipleObjectsReturned
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

settings.configure(DATABASES = {
  'default': { 
    'ENGINE': 'django.db.backends.postgresql',  
    "NAME": 'da4rq88jm0mqau',   
    "USER": 'mwhsdublpfnxzk',   
    "PASSWORD": 
        '5318dc42f30f24c0cd558200d99e66ac33cc906c61eb8465cd9ee69cabca0a9f', 
    "HOST": "ec2-34-251-118-151.eu-west-1.compute.amazonaws.com",   
    "PORT": "5432", 
}
})
django.setup()


from models import Event, Place, Adress, Person


def main():
	with open('c:/Users/anew/litgid/litgid/data/names_coors.json',
				encoding='utf-8') as f:
		data = json.loads(f.read())
		for line in data['data']:
			if line['index'] > 1078:
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
				try:
					event = Event.objects.create(
						description = line['event'],
						date = datetime.strptime(
							' '.join([line['day'], line['hour']]), '%d.%m.%Y %H:%M'),
						place = place,
						adress = adress,
						)
				except:
					event = Event.objects.create(
						description = line['event'],
						date = datetime.strptime('11.09.2007 20:00', '%d.%m.%Y %H:%M'),
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
	