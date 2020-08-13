import json
import django
from django.conf import settings

settings.configure(DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'c:/Users/anew/litgid/litgid/db.sqlite3',
    }
})
django.setup()


from models import Event, Place, Adress, Person


def main():
	with open('c:/Users/anew/litgid/litgid/data/django.json', encoding='utf-8') as f:
		data = json.loads(f.read())

		for line in data:
			event = Event.objects.create(
				description = line['event'],
				date = line['day'],
				place = Place.objects.get_or_create(name=line['place']),
				adress = Adress.objects.get_or_create(name=line['adress'])
				)

			event.save()

if __name__ == '__main__':
	import django
	django.setup()
	main()