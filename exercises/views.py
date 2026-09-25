from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Exercise
from .serializers import ExerciseSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ReliableExercisesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.all().order_by('name')
    serializer_class = ExerciseSerializer
    pagination_class = PageNumberPagination

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


        

