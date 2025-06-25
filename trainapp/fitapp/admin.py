from django.contrib import admin
from .models import *

admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(WorkoutExercise)
admin.site.register(Dprogram)
admin.site.register(ProgramExercise)
admin.site.register(WorkoutResult)
admin.site.register(WorkoutResultSet)
admin.site.register(FutureWorkout)
admin.site.register(FutureWorkoutExercise)