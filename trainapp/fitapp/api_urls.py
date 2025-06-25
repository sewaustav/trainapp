from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'exercise', FitapplistViewSet, basename='exercise')
router.register(r'workout', WorkoutlistViewSet, basename='workout')
router.register(r'workout_exercise', WorkoutExerciselistViewSet, basename='workout_exercise')
router.register(r'dprogram', DprogramlistViewSet, basename='dprogram')
router.register(r'program_exercise', ProgramExerciselistViewSet, basename='program_exercise')
router.register(r'workout_result', WorkoutResultlistViewSet, basename='workout_result')
router.register(r'workout_result_set', WorkoutResultSetlistViewSet, basename='workout_result_set')
router.register(r'schedule', FutureWorkoutViewSet, basename='schedule')
router.register(r'schedule_exercises', FutureWorkoutExerciseViewSet, basename='schedule_exercises')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/next_training/', get_next_training, name='next'),
]