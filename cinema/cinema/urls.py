from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('user/', include('user.urls')),
    path('cms/', include('cms.urls')),
]

if settings.DEBUG:
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
