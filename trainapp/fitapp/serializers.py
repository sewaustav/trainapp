from rest_framework import serializers
from .models import *

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = '__all__'

class DprogramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dprogram
        fields = ['id', 'name', 'description', 'type_of_program']

class ProgramExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramExercise
        fields = '__all__'

class WorkoutResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutResult
        fields = '__all__'

class WorkoutResultSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutResultSet
        fields = '__all__'

class FutureWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureWorkout
        fields = '__all__'

class FutureWorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureWorkoutExercise
        field = '__all__'