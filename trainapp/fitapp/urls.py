from .views import *
from django.urls import path

urlpatterns = [
    path('', mainpage, name='mainpage'),
    path('constructor', constructor, name='constructor'),
    path('program/<str:program_name>', WorkoutFunc, name='tr'),
    path('program-list', ProgramList.as_view(), name='program-list'),
    path('program/view/<str:program_name>', DetailProgram, name='dprogram')
]