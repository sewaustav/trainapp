from .views import *
from django.urls import path

urlpatterns = [
    path('', mainpage, name='mainpage'),
]