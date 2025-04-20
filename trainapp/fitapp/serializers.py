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
        fields = '__all__'

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