from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .views import ReliableExercisesViewSet

router = DefaultRouter()
router.register(r'exercises', ReliableExercisesViewSet, basename='exercise')


urlpatterns = [
    path('', include(router.urls)),
]