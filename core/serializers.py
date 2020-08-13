from rest_framework import serializers

from .models import Event, Place, Adress

class EventSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Event
		fields = '__all__'


class PlaceSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Place
		fields = "__all__"

class AdressSerializer(serializers.HyperlinkedModelSerializer):
	
	class Meta:
		model = Adress
		fields = "__all__"