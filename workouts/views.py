from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Workout, WorkoutExercise, WorkoutSession, ExerciseResult
from .serializers import WorkoutSerializer, WorkoutExerciseSerializer, WorkoutSessionSerializer, WorkoutCompletionSerializer, WorkoutHistorySerializer, ReportDateRangeSerializer
from workouts.permissions import IsOwner, IsOwnerNoUserField
from django.shortcuts import get_object_or_404
from exercises.models import Exercise
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F, ExpressionWrapper, DecimalField, Sum, Max



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

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        session = self.get_object()
        if session.status == "completed":
            raise ValidationError({"status": "This session has already been completed."})
        if session.status == "cancelled":
            raise ValidationError({"status": "A cancelled session cannot be completed."})
        ser = WorkoutCompletionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ids = set()
        results = ser.validated_data["results"]
        for result in results:
            workout_exercise_id = result["workout_exercise"].id
            if workout_exercise_id in ids:
                raise ValidationError({"results": "Each workout exercise can only appear once."})
            ids.add(workout_exercise_id)
            if result["workout_exercise"].workout_id != session.workout_id:
                raise ValidationError({"results": "This exercise does not belong to the sessions workout"})
        expected_ids = set()
        for workout_exercise in session.workout.workout_exercises.all():
            expected_ids.add(workout_exercise.id)
        if expected_ids != ids:
            raise ValidationError({"results": "Provide exactly one result for each exercise in the workout."})
        with transaction.atomic():
            for result in results:
                ExerciseResult.objects.create(
                    workout_session=session,
                    **result,
                )
            session.note = ser.validated_data.get("note", session.note)
            session.total_duration = ser.validated_data.get(
                "total_duration",
                session.total_duration,
            )
            session.status = "completed"
            session.completed_at = timezone.now()
            session.save()
        return Response({"Completed": "Successfully completed"})

    @action(detail=False, methods=['get'])
    def history(self, request, pk=None):
        queryset = (
            self.get_queryset()
            .filter(status="completed")
            .prefetch_related("exercise_results")
            .order_by("-completed_at")
        )
        page = self.paginate_queryset(queryset)
        ser = WorkoutHistorySerializer(page, many=True)
        return self.get_paginated_response(ser.data)

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

    @action(detail=False, methods=['get'])
    def completed_workouts_report(self, request):
        data = ReportDateRangeSerializer(data=request.query_params)
        data.is_valid(raise_exception=True)
        start_date = data.validated_data["start_date"]
        end_date = data.validated_data["end_date"]
        queryset = (
            WorkoutSession.objects
            .filter(status="completed", completed_at__date__range=(start_date, end_date), workout__user=request.user)
        )
        count = queryset.count()
        return Response({
            "start_date": start_date,
            "end_date": end_date,
            "completed_workouts": count,
        })

    @action(detail=False, methods=['get'])
    def training_volume_report(self, request):
        data = ReportDateRangeSerializer(data=request.query_params)
        data.is_valid(raise_exception=True)
        start_date = data.validated_data["start_date"]
        end_date = data.validated_data["end_date"]
        queryset = (
            ExerciseResult.objects
            .filter(workout_session__status="completed", workout_session__completed_at__date__range=(start_date, end_date), workout_session__workout__user=request.user)
            .annotate(
                result_volume=ExpressionWrapper(
                    F("sets_completed")
                    * F("reps_completed")
                    * F("weight_completed"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            )
            .values("exercise_id", "exercise__name")
            .annotate(total_volume=Sum("result_volume", default=0)) 
            .order_by("exercise__name")
        )
        return Response({
            "start_date": start_date,
            "end_date": end_date,
            "results": list(queryset),
        })

    @action(detail=False, methods=['get'])
    def highest_weight_report(self, request):
        data = ReportDateRangeSerializer(data=request.query_params)
        data.is_valid(raise_exception=True)
        start_date = data.validated_data["start_date"]
        end_date = data.validated_data["end_date"]
        queryset = (
            ExerciseResult.objects
            .filter(workout_session__status="completed", workout_session__completed_at__date__range=(start_date, end_date), workout_session__workout__user=request.user)
            .values("exercise_id", "exercise__name")
            .annotate(highest_weight=Max("weight_completed"))
            .order_by("exercise__name")
        )
        return Response({
            "start_date": start_date,
            "end_date": end_date,
            "results": list(queryset),
        })
        
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
        if current.status != "completed" and new_status == "completed":
            raise ValidationError({
                "status": "Use the completion endpoint to complete a session."
            })
        serializer.save()
