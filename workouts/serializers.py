from workouts.models import Workout, WorkoutExercise, WorkoutSession, ExerciseResult
from rest_framework import serializers
from django.core.validators import MinValueValidator
from datetime import timedelta
from rest_framework.exceptions import ValidationError

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = '__all__'
        read_only_fields = ("workout", "exercise",)

class WorkoutSerializer(serializers.ModelSerializer):
    workout_exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Workout
        fields = ["id", "name", "created_at", "description", "user", "workout_exercises"]
        read_only_fields = ("user",)

class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = '__all__'
        read_only_fields = ("workout", "completed_at",)

class ExerciseResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseResult
        fields = '__all__'
        read_only_fields = ("workout_session", "exercise",)

class WorkoutCompletionSerializer(serializers.Serializer):
    note = serializers.CharField(
            max_length=120,
            allow_blank=True,
            required=False,
        )
    total_duration = serializers.DurationField(allow_null=True, required=False, validators=[MinValueValidator(timedelta(0))])
    results = ExerciseResultSerializer(many=True, allow_empty=False)

class WorkoutHistorySerializer(serializers.ModelSerializer):
    exercise_results = ExerciseResultSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutSession
        fields = [
            "id",
            "workout",
            "scheduled_at",
            "status",
            "completed_at",
            "note",
            "total_duration",
            "exercise_results",
        ]
        read_only_fields = (
            "id", 
            "workout",
            "scheduled_at",
            "status",
            "completed_at",
            "note",
            "total_duration",
        )

class ReportDateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    def validate(self, attrs):
        if attrs["start_date"] > attrs["end_date"]:
            raise ValidationError({"date": "The start date cannot be after the end date."})
        return attrs

class WorkoutCompletionResponseSerializer(serializers.Serializer):
    Completed = serializers.CharField()

class CompletedWorkoutsReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    completed_workouts = serializers.IntegerField()

class TrainingVolumeResultSerializer(serializers.Serializer):
    exercise_id = serializers.IntegerField()
    exercise__name = serializers.CharField()
    total_volume = serializers.FloatField()

class TrainingVolumeReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    results = TrainingVolumeResultSerializer(many=True)

class HighestWeightResultSerializer(serializers.Serializer):
    exercise_id = serializers.IntegerField()
    exercise__name = serializers.CharField()
    highest_weight = serializers.FloatField()

class HighestWeightReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    results = HighestWeightResultSerializer(many=True)