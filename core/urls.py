from django.urls import include, path
from rest_framework import routers
from . import views
from .views import EventListView, PlaceListView, \
    EventDetailView, PlaceDetailView, \
    PersonListView, NormalPersonListView, PersonDetailView, \
    FoliumView
from .views import PersonUpdate, PersonDelete, EventCreateView, EventUpdate

handler404 = views.custom_handler404
handler500 = views.custom_handler500


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
    path('event_create', EventCreateView.as_view(), name='event_create'),
    path('places', PlaceListView.as_view(), name='places'),
    path('events', EventListView.as_view(), name='events'),
    path('persons', PersonListView.as_view(), name='persons'),
    path('persons_order', NormalPersonListView.as_view(), name='persons_order'),
    path('event/<pk>/', EventDetailView.as_view(), name='one_event'),
    path('place/<pk>/', PlaceDetailView.as_view(), name='one_place'),
    path('person/<pk>/', PersonDetailView
         .as_view(), name='one_person'),
    path('person_add/<int:event_id>/', views.update_event_with_person,
        name='person_add'),
    path('person_update/<pk>/', PersonUpdate.as_view(), name='person_update'),
    path('person_delete/<pk>', PersonDelete.as_view(), name='person_delete'),
    path('event_edit/<pk>/', EventUpdate.as_view(), name="event_edit"),
    path('edit_persons/<int:event_id>/', views.edit_persons,
        name='edit_persons'),
    path('map', FoliumView.as_view(), name='map'),
    path('api/', include(router.urls)),
    path('api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
]
