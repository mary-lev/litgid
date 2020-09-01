from django.urls import include, path
from rest_framework import routers
from . import views
from .views import EventListView, PlaceListView,\
					EventDetailView, PlaceDetailView,\
					PersonListView, PersonDetailView, \
					PersonUpdate, PersonDelete,\
					EventUpdate, FoliumView


router = routers.DefaultRouter()
router.register(r'api_events', views.EventViewSet)
router.register(r'api_places', views.PlaceViewSet)
router.register(r'api_adresses', views.AdressViewSet)
router.register(r'api_persons', views.PersonViewSet)

app_name = 'core'
urlpatterns = [
	path('', views.index, name='index'),
	path('research', views.research, name='research'),
	path('calendar/<int:year>/<int:month>', views
		.new_calendar, name='calendar'),
	path('places', PlaceListView.as_view(), name='places'),
	path('events', EventListView.as_view(), name='events'),
	path('persons', PersonListView.as_view(), name='persons'),
	path('event/<pk>/', EventDetailView.as_view(), name='one_event'),
	path('place/<pk>/', PlaceDetailView.as_view(), name='one_place'),
	path('person/<pk>/', PersonDetailView
		.as_view(), name='one_person'),
	path('person_edit/<pk>/', PersonUpdate.as_view(), name='person_edit'),
	path('person_delete/<pk>', PersonDelete.as_view(), name='person_delete'),
	path('event_edit/<pk>/', EventUpdate.as_view(), name="event_edit"),
	path('map', FoliumView.as_view(), name='map'),
	path('api/', include(router.urls)),
	path('api-auth/', include(
		'rest_framework.urls', namespace='rest_framework')),
]
