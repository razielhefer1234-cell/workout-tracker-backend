from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from exercises.models import Exercise
from workouts.models import Workout, WorkoutExercise, WorkoutSession


class WorkoutCreationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="alex@example.com",
            first_name="Alex",
            last_name="Smith",
            password="Strong-passphrase-7845!",
        )
        self.squat = Exercise.objects.create(name="Squat")
        self.push_up = Exercise.objects.create(name="Push-up")
        self.workout = Workout.objects.create(user=self.user, name="Full body")

    def workout_exercise(self, exercise, order, **overrides):
        values = {
            "workout": self.workout,
            "exercise": exercise,
            "order": order,
            "sets": 3,
            "reps": 8,
            "rest_seconds": 90,
            "weight": Decimal("40.00"),
        }
        values.update(overrides)
        return WorkoutExercise(**values)

    def test_create_ordered_workout_and_scheduled_session(self):
        first = self.workout_exercise(self.squat, 1)
        first.full_clean()
        first.save()

        second = self.workout_exercise(self.push_up, 2)
        second.full_clean()
        second.save()

        session = WorkoutSession(
            workout=self.workout,
            scheduled_at=timezone.now() + timedelta(days=1),
        )
        session.full_clean()
        session.save()

        self.assertTrue(self.user.check_password("Strong-passphrase-7845!"))
        self.assertEqual(
            list(
                self.workout.workout_exercises.values_list("order", "exercise__name")
            ),
            [(1, "Squat"), (2, "Push-up")],
        )
        self.assertEqual(session.workout.user, self.user)
        self.assertEqual(session.status, "scheduled")

    def test_invalid_planned_values_and_duplicates_are_rejected(self):
        for field, value in (
            ("order", 0),
            ("sets", 0),
            ("reps", 0),
            ("rest_seconds", 0),
            ("weight", Decimal("-1.00")),
        ):
            with self.subTest(field=field):
                item = self.workout_exercise(self.squat, 1, **{field: value})
                with self.assertRaises(ValidationError) as error:
                    item.full_clean()
                self.assertIn(field, error.exception.message_dict)

        first = self.workout_exercise(self.squat, 1)
        first.full_clean()
        first.save()

        with self.assertRaises(ValidationError):
            self.workout_exercise(self.push_up, 1).full_clean()

        with self.assertRaises(ValidationError):
            self.workout_exercise(self.squat, 2).full_clean()
