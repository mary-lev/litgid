from django.conf import settings
from django.contrib import admin
from django.urls import path, include
if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path('', include('core.urls')),
    #path('__debug__', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    ]
  