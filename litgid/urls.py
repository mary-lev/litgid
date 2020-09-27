from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('core.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('admin/', admin.site.urls),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = urlpatterns + [path('__debug__', include(debug_toolbar.urls)), ]
