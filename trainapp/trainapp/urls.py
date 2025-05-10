from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('fitapp.urls')),
                  path('api/', include('fitapp.api_urls')),
                  path('accounts/', include('allauth.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
