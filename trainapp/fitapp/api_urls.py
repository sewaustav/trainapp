from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'exercise', FitapplistViewSet, basename='exercise')
router.register(r'workout', WorkoutlistViewSet, basename='workout')
router.register(r'workout_exercise', WorkoutExerciselistViewSet, basename='workout_exercise')
router.register(r'dprogram', DprogramlistViewSet, basename='dprogram')
router.register(r'program_exercise', ProgramExerciselistViewSet, basename='program_exercise')
router.register(r'workout_result', WorkoutResultlistViewSet, basename='workout_result')
router.register(r'workout_result_set', WorkoutResultSetlistViewSet, basename='workout_result_set')

urlpatterns = [
    path('api/', include(router.urls)),
    # path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/programs/delete/<str:name>', delete_program_by_name, name='delete-pr'),
]