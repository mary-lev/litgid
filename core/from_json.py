import json
from datetime import datetime
import django
from django.conf import settings

from django.core.exceptions import MultipleObjectsReturned


settings.configure(DATABASES = {
   'default': {
    'ENGINE': 'django.db.backends.postgresql',
    "NAME": 'db0ic13kt362fa',
    "USER": 'beytgschuzelxe',
    "PASSWORD":
        'd5d152b6eddab38aabdfefe4e22ca5abc3d69656240c3a101240e240c85e1c47',
    "HOST": "ec2-34-253-148-186.eu-west-1.compute.amazonaws.com",
    "PORT": "5432",
}
})
django.setup()


from models import Event, Place, Adress, Person


def main():
	with open('c:/Users/anew/litgid/litgid/data/test_6_09_2020.json',
				encoding='utf-8') as f:
		data = json.loads(f.read())
		for line in data['data'][:500]:
			print(line)
			place, created = Place.objects.get_or_create(
				name=line['place'])
			adress, created = Adress.objects.get_or_create(
				lon=line['lon'],
				lat=line['lat'],
				name=line['adress']
				)
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
				one = [all if all is not None else '' for all in one]
				try:
					person, created = Person.objects.get_or_create(name=one[0], second_name=one[1], family=one[2])
					event.people.add(person)
				except (MultipleObjectsReturned):
					pass


if __name__ == '__main__':
	import django
	django.setup()
	main()
	