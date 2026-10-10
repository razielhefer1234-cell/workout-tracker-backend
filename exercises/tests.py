from django.test import TestCase
from accounts.models import MyUser
from workouts.models import Workout, WorkoutExercise
from exercises.models import Exercise
from django.urls import reverse

class ExerciseTests(TestCase):
    def test_add_exercise_to_workout_success(self):
        user = MyUser.objects.create_user(
            email='razielhefer@gmail.com',
            password='wWPE4c4HJHJgXZMmhksve2pkp',
            last_name='Arik',
            first_name='Hefer',
        )
        response1 = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer@gmail.com',
                'password': 'wWPE4c4HJHJgXZMmhksve2pkp',
            }
        )
        access_token = response1.json()['access']
        response2 = self.client.post(
            reverse('workout-list'),
            {
                'name': 'Chest Workout',
                'description': 'This Workout is too workout my chest'
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        exercise_create = Exercise.objects.create(name="Push Ups")
        exercise = Exercise.objects.get(name="Push Ups")
        workout = Workout.objects.get(user=user, name='Chest Workout')
        response3 = self.client.post(
            reverse('workout_exercise-list'),
            {
                'order': 1,
                'sets': 3,
                'reps': 3,
                'rest_seconds': 30,
                'workout': workout.id,
                'exercise': exercise.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response3.status_code, 201)
        self.assertTrue(WorkoutExercise.objects.filter(workout=workout, exercise=exercise).exists())
