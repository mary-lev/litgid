from django.urls import include, path
from rest_framework import routers
from . import views
from .views import EventListView


router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'places', views.PlaceViewSet)
router.register(r'adresses', views.AdressViewSet)


urlpatterns = [
	path('', views.index, name='index'),
	path('event/', EventListView.as_view()),
	path('api/', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]