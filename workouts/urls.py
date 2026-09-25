from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .views import ReliableWorkoutViewSet, ReliableWorkoutExerciseViewSet, ReliableWorkoutSessionViewSet

router = DefaultRouter()
router.register(r'workouts', ReliableWorkoutViewSet, basename='workout')
router.register(r'workouts-exercises', ReliableWorkoutExerciseViewSet, basename='workout_exercise')
router.register(r'workouts-sessions', ReliableWorkoutSessionViewSet, basename='workout_session')

urlpatterns = [
    path('', include(router.urls)),
]