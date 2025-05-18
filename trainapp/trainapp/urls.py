from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from fitapp.views import logout_view

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('fitapp.urls')),
                  path('api/', include('fitapp.api_urls')),
                  path('accounts/', include('allauth.urls')),
                  path('logout/', logout_view, name='account_logout'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
