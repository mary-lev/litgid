from rest_framework import serializers
from .models import Event, Place, Adress, Person


class PersonSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='core:person-detail')

	class Meta:
		model = Person
		fields = "__all__"


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='core:place-detail')

	class Meta:
		model = Place
		fields = "__all__"


class AdressSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='core:adress-detail')

	class Meta:
		model = Adress
		fields = "__all__"


class EventSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='core:event-detail')
	place = PlaceSerializer()
	adress = AdressSerializer()
	people = PersonSerializer(many=True, read_only=False)

	class Meta:
		model = Event
		fields = '__all__'
