from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .views import ReliableWorkoutViewSet, ReliableWorkoutExerciseViewSet

router = DefaultRouter()
router.register(r'workouts', ReliableWorkoutViewSet, basename='workout')
router.register(r'workouts-exercises', ReliableWorkoutExerciseViewSet, basename='workoutexercise')


urlpatterns = [
    path('', include(router.urls)),
]