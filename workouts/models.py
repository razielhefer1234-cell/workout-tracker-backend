from django.db import models
from accounts.models import MyUser
from django.core.validators import MinValueValidator
from exercises.models import Exercise
from django.conf import settings
from datetime import timedelta

# Create your models here.
class Workout(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workouts",
        related_query_name="workout",
    )

    exercises = models.ManyToManyField(
        Exercise,
        through="WorkoutExercise",
        related_name="workouts",
        related_query_name="workout",
    )
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Workout"
        verbose_name_plural = "Workouts"
        db_table = "Workout"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_workout_name_per_user",
            )
        ]

class WorkoutExercise(models.Model):
    order = models.IntegerField(validators=[MinValueValidator(1)])
    sets = models.IntegerField(validators=[MinValueValidator(1)])
    reps = models.IntegerField(validators=[MinValueValidator(1)])
    rest_seconds = models.IntegerField(validators=[MinValueValidator(1)])
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    workout = models.ForeignKey(
        Workout,
        related_name="workout_exercises",
        related_query_name="workout_exercise",
        on_delete=models.CASCADE,
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="workout_exercises",
        related_query_name="workout_exercise",
    )

    def __str__(self):
        return f"{self.workout.name} — {self.exercise.name}"

    class Meta:
        ordering = ["workout", "order"]
        verbose_name = "WorkoutExercise"
        verbose_name_plural = "WorkoutExercises"
        db_table = "WorkoutExercise"
        constraints = [
            models.UniqueConstraint(
                fields=["workout", "order"],
                name="unique_order_per_workout",
            ),
            models.UniqueConstraint(
                fields=["workout", "exercise"],
                name="unique_exercise_per_workout",
            ),
        ]

class WorkoutSession(models.Model):
    scheduled_at = models.DateTimeField()
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("cancelled", "Cancelled"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled",
    )
    completed_at = models.DateTimeField(blank=True, null=True)
    note = models.CharField(max_length=120, blank=True)
    total_duration = models.DurationField(blank=True, null=True, validators=[MinValueValidator(timedelta(0))])
    workout = models.ForeignKey(
        Workout,
        on_delete=models.PROTECT,
        related_name="workout_sessions",
        related_query_name="workout_session",
    )
    def __str__(self):
        return self.workout.name

    class Meta:
        ordering = ["-scheduled_at"]
        verbose_name = "Workout session"
        verbose_name_plural = "Workout sessions"
        db_table = "WorkoutSession"

class ExerciseResult(models.Model):
    sets_completed = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    reps_completed = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    duration = models.DurationField(
        blank=True,
        null=True,
        validators=[MinValueValidator(timedelta(0))],
    )

    weight_completed = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )

    note = models.CharField(
        max_length=120,
        blank=True,
    )
 
    exercise_order = models.PositiveIntegerField(editable=False)
    
    workout_session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.PROTECT,
        related_name="exercise_results",
        related_query_name="exercise_result",
    )

    workout_exercise = models.ForeignKey(
        WorkoutExercise,
        on_delete=models.PROTECT,
        related_name="exercise_results",
        related_query_name="exercise_result",
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.PROTECT,
        related_name="exercise_results",
        editable=False,
    )
    
    def save(self, *args, **kwargs):
        
        if self._state.adding:
            self.exercise_order = self.workout_exercise.order
            self.exercise_id = self.workout_exercise.exercise_id
            
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["workout_session", "exercise_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["workout_session", "workout_exercise"],
                name="unique_exercise_result_per_session",
           )
        ]