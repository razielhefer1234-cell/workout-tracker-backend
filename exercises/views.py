from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Exercise
from .serializers import ExerciseSerializer


class ReliableExercisesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.all().order_by('name')
    serializer_class = ExerciseSerializer
    pagination_class = PageNumberPagination


        

