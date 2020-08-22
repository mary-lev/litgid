from rest_framework import serializers
from .models import Event, Place, Adress


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='core:place-detail')

	class Meta:
		model = Place
		fields = "__all__"


class AdressSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='core:adress-detail')

	class Meta:
		model = Adress
		fields = "__all__"


class EventSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='core:event-detail')
	place = PlaceSerializer()
	adress = AdressSerializer()

	class Meta:
		model = Event
		fields = '__all__'