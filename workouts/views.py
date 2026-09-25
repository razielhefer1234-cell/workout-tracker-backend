from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Workout, WorkoutExercise, WorkoutSession
from .serializers import WorkoutSerializer, WorkoutExerciseSerializer, WorkoutSessionSerializer
from workouts.permissions import IsOwner, IsOwnerNoUserField
from django.shortcuts import get_object_or_404
from exercises.models import Exercise
from rest_framework.exceptions import ValidationError
from django.utils import timezone


class ReliableWorkoutViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner] 
    queryset = Workout.objects.all().order_by('name')
    serializer_class = WorkoutSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return (
            Workout.objects
            .filter(user=self.request.user)
            .prefetch_related("workout_exercises__exercise")
            .select_related("user")
            .order_by("name")
        )

    def perform_create(self, serializer):
        name = serializer.validated_data["name"]
        if Workout.objects.filter(user=self.request.user, name=name).exists():
            raise ValidationError({"name": "You already have a workout with this name."})
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        current = serializer.instance
        name = serializer.validated_data.get("name")
        if name is not None:
            if Workout.objects.filter(user=self.request.user, name=name).exclude(pk=current.pk).exists():
                raise ValidationError({"name": "You already have another workout with this name."})
        serializer.save()
        
class ReliableWorkoutExerciseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerNoUserField] 
    queryset = WorkoutExercise.objects.all().order_by('order')
    serializer_class = WorkoutExerciseSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return (
            WorkoutExercise.objects
            .filter(workout__user=self.request.user)
            .select_related("workout", "exercise")
            .order_by("order")
        )

    def perform_create(self, serializer):
        raw_workout_id = self.request.data.get("workout")
        raw_exercise_id = self.request.data.get("exercise")
        if not raw_workout_id:
            raise ValidationError({"workout": "This field is required."})
        if not raw_exercise_id:
            raise ValidationError({"exercise": "This field is required."})
        try:
            workout_id = int(self.request.data.get("workout"))
        except (TypeError, ValueError):
            raise ValidationError({"workout": "Workout ID must be an integer."})
        try:
            exercise_id = int(self.request.data.get("exercise"))
        except (TypeError, ValueError):
            raise ValidationError({"exercise": "Exercise ID must be an integer."})
        workout = get_object_or_404(
            Workout,
            pk=workout_id,
            user=self.request.user
        )
        exercise = get_object_or_404(
            Exercise,
            pk=exercise_id,
        )
        order = serializer.validated_data["order"]
        if WorkoutExercise.objects.filter(order=order, workout=workout).exists():
            raise ValidationError({"order": "This order is already used in this workout."})
        if WorkoutExercise.objects.filter(workout=workout, exercise=exercise).exists():
            raise ValidationError({"exercise": "This exercise is already in this workout."})
        serializer.save(workout=workout, exercise=exercise)

    def perform_update(self, serializer):
        current = serializer.instance
        new_order = serializer.validated_data.get("order")
        if new_order is not None:
            if WorkoutExercise.objects.filter(workout=current.workout, order=new_order).exclude(pk=current.pk).exists():
                raise ValidationError({"order": "This order is already used in this workout."})
        serializer.save()

class ReliableWorkoutSessionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerNoUserField] 
    queryset = WorkoutSession.objects.all().order_by('-scheduled_at')
    serializer_class = WorkoutSessionSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        status = self.request.query_params.get("status")
        scheduled_at = self.request.query_params.get("scheduled_at")
        if status is not None and scheduled_at is not None:
            return(
                WorkoutSession.objects
                .filter(workout__user=self.request.user, status=status, scheduled_at__date=scheduled_at)
                .select_related("workout")
                .order_by("scheduled_at")
            )
        if status is not None:
            return(
                WorkoutSession.objects
                .filter(workout__user=self.request.user, status=status)
                .select_related("workout")
                .order_by("scheduled_at")
            )
        if scheduled_at is not None:
            return(
                WorkoutSession.objects
                .filter(workout__user=self.request.user, scheduled_at__date=scheduled_at)
                .select_related("workout")
                .order_by("scheduled_at")
            )

        return(
            WorkoutSession.objects
            .filter(workout__user=self.request.user)
            .select_related("workout")
            .order_by("scheduled_at")
        )
        
    
    def perform_create(self, serializer):
        requested_status = serializer.validated_data.get("status", "scheduled")
        raw_workout_id = self.request.data.get("workout")
        scheduled_at = serializer.validated_data["scheduled_at"]
        if requested_status != "scheduled":
            raise ValidationError({"status": "A new session must start as scheduled."})
        if scheduled_at is not None and scheduled_at < timezone.now():
            raise ValidationError("The scheduled date and time must be in the future.")     
        if not scheduled_at:
            raise ValidationError({"scheduled_at": "This field is required."})
        if not raw_workout_id:
            raise ValidationError({"workout": "This field is required."})
        try:
            workout_id = int(self.request.data.get("workout"))
        except (TypeError, ValueError):
            raise ValidationError({"workout": "Workout ID must be an integer."})
        workout = get_object_or_404(
            Workout,
            pk=workout_id,
            user=self.request.user
        )
        serializer.save(workout=workout)

    def perform_update(self, serializer):
        current = serializer.instance
        new_status = serializer.validated_data.get("status", current.status)
        scheduled_at = serializer.validated_data.get("scheduled_at")
        if scheduled_at is not None and scheduled_at < timezone.now():
            raise ValidationError({"The scheduled date and time must be in the future."})
        if current.status == "completed" and new_status != "completed":
            raise ValidationError({"status": "A completed session's status cannot be changed."})
        serializer.save()
        