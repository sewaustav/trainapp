from django.shortcuts import render, redirect

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def mainpage(request):
    return render(request, 'fitapp/main.html')


# api
@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) # временная фича пока не завезут регистрацию
def delete_program_by_name(request, name):
    try:
        program = Dprogram.objects.get(name=name)
        program.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Dprogram.DoesNotExist:
        return Response({"error": "Программа не найдена"}, status=status.HTTP_404_NOT_FOUND)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff


class FitapplistViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAdminOrReadOnly]

class WorkoutlistViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

class WorkoutExerciselistViewSet(viewsets.ModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer
    permission_classes = [IsAuthenticated]

class DprogramlistViewSet(viewsets.ModelViewSet):
    queryset = Dprogram.objects.all()
    serializer_class = DprogramSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProgramExerciselistViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ProgramExercise.objects.all()
        program_id = self.request.query_params.get('program')
        if program_id:
            queryset = queryset.filter(program_id=program_id)
        return queryset




class WorkoutResultlistViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutResult.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutResultSetlistViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutResultSetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = WorkoutResultSet.objects.all()
        workout_id = self.request.query_params.get('workout')
        if workout_id:
            queryset = queryset.filter(workout_id=workout_id)
        return queryset


