from django.shortcuts import render, redirect


from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def mainpage(request):
    return render(request, 'fitapp/main.html')


# api
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
        return WorkoutResult.objects.filter(user=self.request.user).order_by('-id')

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


class FutureWorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = FutureWorkoutSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        current_datetime = datetime.now()
        return FutureWorkout.objects.filter(user=self.request.user, date__gt=current_datetime).order_by('date')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_next_training(request):
    try:
        next_workout = (FutureWorkout.objects.filter(user=request.user).order_by('date').first())
        if next_workout:
            serializer = FutureWorkoutSerializer(next_workout)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'details': 'You have not any training in your plan'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FutureWorkoutExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = FutureWorkoutExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = FutureWorkoutExercise.objects.all()
        workout_id = self.request.query_params.get('workout')
        if workout_id:
            queryset = queryset.filter(workout_id=workout_id)
        return queryset



