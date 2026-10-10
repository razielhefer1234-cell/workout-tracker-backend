from django.test import TestCase
from accounts.models import MyUser
from workouts.models import Workout, WorkoutSession, WorkoutExercise, ExerciseResult
from exercises.models import Exercise
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone

class WorkoutTests(TestCase):
    def test_create_workout_success(self):
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
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(Workout.objects.count(), 1)
        workout = Workout.objects.get(user=user, name='Chest Workout')
        self.assertEqual(workout.user, user)

    def test_get_workout_detail(self):
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
        workout = Workout.objects.get(user=user, name='Chest Workout')
        response3 = self.client.get(
            reverse('workout-detail', args=[workout.id]),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response3.status_code, 200)
        self.assertIn('name', response3.json())
        self.assertIn('description', response3.json())
        self.assertIn('user', response3.json())
        self.assertEqual(response3.json()['user'], user.id)

    def test_update_workout_success(self):
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
        workout = Workout.objects.get(user=user, name='Chest Workout')
        response3 = self.client.patch(
            reverse('workout-detail', args=[workout.id]),
            {
                'name': 'Chest_Workout',
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response3.status_code, 200)
        updated_workout = Workout.objects.get(id=workout.id)
        self.assertEqual(updated_workout.name, 'Chest_Workout')

    def test_user_cannot_update_other_users_workout(self):
        user_A = MyUser.objects.create_user(
            email='razielhefer1@gmail.com',
            password='wWPE4c4H66HJgXZMmhksve2pkp',
            last_name='Raziel',
            first_name='Hefer',
        )
        user_B = MyUser.objects.create_user(
            email='razielhefer@gmail.com',
            password='wWPE4c4HJHJgXZMmhksve2pkp',
            last_name='Arik',
            first_name='Hefer',
        )
        response1_A = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer1@gmail.com',
                'password': 'wWPE4c4H66HJgXZMmhksve2pkp',
            }
        )
        response1_B = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer@gmail.com',
                'password': 'wWPE4c4HJHJgXZMmhksve2pkp',
            }
        )   
        access_token_A = response1_A.json()['access']
        access_token_B = response1_B.json()['access']
        response2_A = self.client.post(
            reverse('workout-list'),
            {
                'name': 'Chest Workout',
                'description': 'This Workout is too workout my chest'
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_A}",
        )
        workout = Workout.objects.get(user=user_A, name='Chest Workout')
        response3_B = self.client.patch(
            reverse('workout-detail', args=[workout.id]),
            {
                'name': 'Chest_Workout',
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_B}",
        )
        self.assertEqual(response3_B.status_code, 404)
        updated_workout = Workout.objects.get(id=workout.id)
        self.assertEqual(updated_workout.name, 'Chest Workout')
     
    def test_workout_name_must_be_unique_per_user(self):
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
        response3 = self.client.post(
            reverse('workout-list'),
            {
                'name': 'Chest Workout',
                'description': 'This Workout is too workout my chest'
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response3.status_code, 400)

class WorkoutSessionTests(TestCase):
    def test_create_workout_session_success(self):
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
        workout = Workout.objects.get(user=user, name='Chest Workout')
        future_date = timezone.now() + timedelta(days=1)
        response3 = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': future_date.isoformat(),
                'status': 'scheduled',
                'workout': workout.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response3.status_code, 201)
        self.assertEqual(WorkoutSession.objects.count(), 1)

    def test_cannot_create_workout_session_in_past(self):  
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
        workout = Workout.objects.get(user=user, name='Chest Workout')
        response3 = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': '2025-01-15T18:00:00Z',
                'status': 'scheduled',
                'workout': workout.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response3.status_code, 400)
        self.assertEqual(WorkoutSession.objects.count(), 0)

    def test_cannot_change_cancelled_session_to_completed_with_patch(self):
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
        workout = Workout.objects.get(user=user, name='Chest Workout')
        future_date = timezone.now() + timedelta(days=1)
        response3 = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': future_date.isoformat(),
                'status': 'scheduled',
                'workout': workout.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        workout_session = WorkoutSession.objects.get(workout=workout.id)
        response4 = self.client.patch(
            reverse('workout_session-detail', args=[workout_session.id]),
            {
                'status': 'cancelled',
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        response5 = self.client.patch(
            reverse('workout_session-detail', args=[workout_session.id]),
            {
                'status': 'completed',
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response5.status_code, 400)
        updated_workout_session = WorkoutSession.objects.get(workout=workout.id)
        self.assertEqual(updated_workout_session.status, 'cancelled')

    def test_complete_workout_session_success(self):
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
        workout_exercise = WorkoutExercise.objects.get(workout=workout.id, exercise=exercise.id)
        future_date = timezone.now() + timedelta(days=1)
        response4 = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': future_date.isoformat(),
                'status': 'scheduled',
                'workout': workout.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        workout_session = WorkoutSession.objects.get(workout=workout.id)
        response5 = self.client.post(
            reverse('workout_session-complete', args=[workout_session.id]),
            {
                'results': [
                    {  
                        'workout_exercise': workout_exercise.id,
                        'sets_completed': 2,
                        'reps_completed': 3,
                    },
                ],
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response5.status_code, 200)
        updated_workout_session = WorkoutSession.objects.get(workout=workout.id)
        self.assertEqual(updated_workout_session.status, 'completed')
        self.assertNotEqual(updated_workout_session.completed_at, None)
        self.assertEqual(ExerciseResult.objects.count(), 1)

    def test_cannot_complete_workout_session_twice(self):
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
        workout_exercise = WorkoutExercise.objects.get(workout=workout.id, exercise=exercise.id)
        future_date = timezone.now() + timedelta(days=1)
        response4 = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': future_date.isoformat(),
                'status': 'scheduled',
                'workout': workout.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        workout_session = WorkoutSession.objects.get(workout=workout.id)
        response5 = self.client.post(
            reverse('workout_session-complete', args=[workout_session.id]),
            {
                'results': [
                    {  
                        'workout_exercise': workout_exercise.id,
                        'sets_completed': 2,
                        'reps_completed': 3,
                    },
                ],
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response5.status_code, 200)
        response6 = self.client.post(
            reverse('workout_session-complete', args=[workout_session.id]),
            {
                'results': [
                    {  
                        'workout_exercise': workout_exercise.id,
                        'sets_completed': 2,
                        'reps_completed': 3,
                    },
                ],
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response6.status_code, 400)
        updated_workout_session = WorkoutSession.objects.get(workout=workout.id)
        self.assertEqual(updated_workout_session.status, "completed")
        self.assertEqual(ExerciseResult.objects.count(), 1)

    def test_cannot_complete_cancelled_session_through_complete_endpoint(self):
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
        workout_exercise = WorkoutExercise.objects.get(workout=workout.id, exercise=exercise.id)
        future_date = timezone.now() + timedelta(days=1)
        response4 = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': future_date.isoformat(),
                'status': 'scheduled',
                'workout': workout.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        workout_session = WorkoutSession.objects.get(workout=workout.id)
        response5 = self.client.patch(
            reverse('workout_session-detail', args=[workout_session.id]),
            {
                'status': 'cancelled',
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        response6 = self.client.post(
            reverse('workout_session-complete', args=[workout_session.id]),
            {
                'results': [
                    {  
                        'workout_exercise': workout_exercise.id,
                        'sets_completed': 2,
                        'reps_completed': 3,
                    },
                ],
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response6.status_code, 400)
        updated_workout_session = WorkoutSession.objects.get(workout=workout.id)
        self.assertEqual(updated_workout_session.status, 'cancelled')
        self.assertEqual(ExerciseResult.objects.count(), 0)

    def test_cannot_complete_session_with_exercise_from_another_workout(self):
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
        response2_A = self.client.post(
            reverse('workout-list'),
            {
                'name': 'Chest Workout',
                'description': 'This Workout is too workout my chest'
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        response2_B = self.client.post(
            reverse('workout-list'),
            {
                'name': 'Leg Workout',
                'description': 'This Workout is too workout my Leg'
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        exercise_create_a = Exercise.objects.create(name="Push Ups")
        exercise_A = Exercise.objects.get(name="Push Ups")
        exercise_create_B = Exercise.objects.create(name="Leg Ups")
        exercise_B = Exercise.objects.get(name="Leg Ups")
        workout_A = Workout.objects.get(user=user, name='Chest Workout')
        workout_B = Workout.objects.get(user=user, name='Leg Workout')
        response3_A = self.client.post(
            reverse('workout_exercise-list'),
            {
                'order': 1,
                'sets': 3,
                'reps': 3,
                'rest_seconds': 30,
                'workout': workout_A.id,
               'exercise': exercise_A.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        response3_B = self.client.post(
            reverse('workout_exercise-list'),
            {
                'order': 1,
                'sets': 3,
                'reps': 3,
                'rest_seconds': 30,
                'workout': workout_B.id,
               'exercise': exercise_B.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        workout_exercise_B = WorkoutExercise.objects.get(workout=workout_B.id, exercise=exercise_B.id)
        future_date = timezone.now() + timedelta(days=1)
        response4_A = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': future_date.isoformat(),
                'status': 'scheduled',
                'workout': workout_A.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        workout_session_A = WorkoutSession.objects.get(workout=workout_A.id)
        response6_B = self.client.post(
            reverse('workout_session-complete', args=[workout_session_A.id]),
            {
                'results': [
                    {  
                        'workout_exercise': workout_exercise_B.id,
                        'sets_completed': 2,
                        'reps_completed': 3,
                    },
                ],
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response6_B.status_code, 400)
        updated_workout_session_A = WorkoutSession.objects.get(workout=workout_A.id)
        self.assertEqual(updated_workout_session_A.status, 'scheduled')
        self.assertEqual(ExerciseResult.objects.count(), 0)

    def test_cannot_complete_session_with_missing_exercise_result(self):
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
        exercise_create_A = Exercise.objects.create(name="Push Ups")
        exercise_A = Exercise.objects.get(name="Push Ups")
        exercise_create_B = Exercise.objects.create(name="Leg Ups")
        exercise_B = Exercise.objects.get(name="Leg Ups")
        workout = Workout.objects.get(user=user, name='Chest Workout')
        response3_A = self.client.post(
            reverse('workout_exercise-list'),
            {
                'order': 1,
                'sets': 3,
                'reps': 3,
                'rest_seconds': 30,
                'workout': workout.id,
                'exercise': exercise_A.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        response3_B = self.client.post(
            reverse('workout_exercise-list'),
            {
                'order': 2,
                'sets': 3,
                'reps': 3,
                'rest_seconds': 30,
                'workout': workout.id,
                'exercise': exercise_B.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        future_date = timezone.now() + timedelta(days=1)
        response4 = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': future_date.isoformat(),
                'status': 'scheduled',
                'workout': workout.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )  
        workout_exercise_B = WorkoutExercise.objects.get(workout=workout.id, exercise=exercise_B.id)
        workout_session = WorkoutSession.objects.get(workout=workout.id)
        response6 = self.client.post(
            reverse('workout_session-complete', args=[workout_session.id]),
            {
                'results': [
                    {  
                        'workout_exercise': workout_exercise_B.id,
                        'sets_completed': 2,
                        'reps_completed': 3,
                    },
                ],
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        updated_workout_session = WorkoutSession.objects.get(workout=workout.id)
        self.assertEqual(response6.status_code, 400)
        self.assertEqual(updated_workout_session.status, 'scheduled')
        self.assertEqual(ExerciseResult.objects.count(), 0)

    def test_cannot_complete_session_with_duplicate_exercise_results(self):
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
        workout_exercise = WorkoutExercise.objects.get(workout=workout.id, exercise=exercise.id)
        future_date = timezone.now() + timedelta(days=1)
        response4 = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': future_date.isoformat(),
                'status': 'scheduled',
                'workout': workout.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        workout_session = WorkoutSession.objects.get(workout=workout.id)
        response5 = self.client.post(
            reverse('workout_session-complete', args=[workout_session.id]),
            {
                'results': [
                    {  
                        'workout_exercise': workout_exercise.id,
                        'sets_completed': 2,
                        'reps_completed': 3,
                    },
                    {
                        'workout_exercise': workout_exercise.id,
                        'sets_completed': 2,
                        'reps_completed': 3,
                    },
                ],
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response5.status_code, 400)
        updated_workout_session = WorkoutSession.objects.get(workout=workout.id)
        self.assertEqual(updated_workout_session.status, 'scheduled')
        self.assertEqual(ExerciseResult.objects.count(), 0)

    def test_user_cannot_update_other_users_workout_session(self):
        user_A = MyUser.objects.create_user(
            email='razielhefer@gmail.com',
            password='wWPE4c4HJHJgXZMmhksve2pkp',
            last_name='Arik',
            first_name='Hefer',
        )
        user_B = MyUser.objects.create_user(
            email='razielhefer1@gmail.com',
            password='wWPE4h4HJHJgXZMmhksve2pkp',
            last_name='Arik',
            first_name='Hefer',
        )
        response1_A = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer@gmail.com',
                'password': 'wWPE4c4HJHJgXZMmhksve2pkp',
            }
        )
        response1_B = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer1@gmail.com',
                'password': 'wWPE4h4HJHJgXZMmhksve2pkp',
            }
        )
        access_token_A = response1_A.json()['access']
        access_token_B = response1_B.json()['access']
        response2_A = self.client.post(
            reverse('workout-list'),
            {
                'name': 'Chest Workout',
                'description': 'This Workout is too workout my chest'
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_A}",
        )
        workout_A = Workout.objects.get(user=user_A, name='Chest Workout')
        future_date = timezone.now() + timedelta(days=1)
        response4_A = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': future_date.isoformat(),
                'status': 'scheduled',
                'workout': workout_A.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_A}",
        )
        workout_session_A = WorkoutSession.objects.get(workout=workout_A.id)
        response5_B = self.client.patch(
            reverse('workout_session-detail', args=[workout_session_A.id]),
            {
                'status': 'cancelled',
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_B}",
        )
        self.assertEqual(response5_B.status_code, 404)
        updated_workout_session_A = WorkoutSession.objects.get(workout=workout_A.id)
        self.assertEqual(updated_workout_session_A.status, 'scheduled')

    def test_completed_history_remains_accurate_after_workout_exercise_edit(self):
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
        workout_exercise = WorkoutExercise.objects.get(workout=workout.id, exercise=exercise.id)
        future_date = timezone.now() + timedelta(days=1)
        response4 = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': future_date.isoformat(),
                'status': 'scheduled',
                'workout': workout.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        workout_session = WorkoutSession.objects.get(workout=workout.id)
        response5 = self.client.post(
            reverse('workout_session-complete', args=[workout_session.id]),
            {
                'results': [
                    {  
                        'workout_exercise': workout_exercise.id,
                        'sets_completed': 2,
                        'reps_completed': 3,
                    },
                ],
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        response6 = self.client.patch(
            reverse('workout_exercise-detail', args=[workout_exercise.id]),
            {
                'order': 3,
                'sets': 1,
                'reps': 5,
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response6.status_code, 200)
        response7 = self.client.get(
            reverse('workout_session-history'),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response7.status_code, 200)
        response7_json = response7.json()
        history_result = response7_json['results'][0]['exercise_results'][0]
        self.assertEqual(history_result['exercise_order'], 1)
        self.assertEqual(history_result['reps_completed'], 3)
        self.assertEqual(history_result['sets_completed'], 2)

    def test_user_cannot_see_other_users_completed_session_in_history(self):
        user_A = MyUser.objects.create_user(
            email='razielhefer@gmail.com',
            password='wWPE4c4HJHJgXZMmhksve2pkp',
            last_name='Arik',
            first_name='Hefer',
        )
        user_B = MyUser.objects.create_user(
            email='razielhefer1@gmail.com',
            password='wWPE4h4HJHJgXZMmhksve2pkp',
            last_name='Arik',
            first_name='Hefer',
        )
        response1_A = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer@gmail.com',
                'password': 'wWPE4c4HJHJgXZMmhksve2pkp',
            }
        )
        response1_B = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer1@gmail.com',
                'password': 'wWPE4h4HJHJgXZMmhksve2pkp',
            }
        )
        access_token_A = response1_A.json()['access']
        access_token_B = response1_B.json()['access']
        response2_A = self.client.post(
            reverse('workout-list'),
            {
                'name': 'Chest Workout',
                'description': 'This Workout is too workout my chest'
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_A}",
        )
        exercise_create = Exercise.objects.create(name="Push Ups")
        exercise = Exercise.objects.get(name="Push Ups")
        workout_A = Workout.objects.get(user=user_A, name='Chest Workout')
        response3_A = self.client.post(
            reverse('workout_exercise-list'),
            {
                'order': 1,
                'sets': 3,
                'reps': 3,
                'rest_seconds': 30,
                'workout': workout_A.id,
               'exercise': exercise.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_A}",
        )
        workout_exercise_A = WorkoutExercise.objects.get(workout=workout_A)
        future_date = timezone.now() + timedelta(days=1)
        response4_A = self.client.post(
            reverse('workout_session-list'),
            {
                'scheduled_at': future_date.isoformat(),
                'status': 'scheduled',
                'workout': workout_A.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_A}",
        )
        workout_session_A = WorkoutSession.objects.get(workout=workout_A.id)
        response5_A = self.client.post(
            reverse('workout_session-complete', args=[workout_session_A.id]),
            {
                'results': [
                    {
                        'workout_exercise': workout_exercise_A.id,
                        'sets_completed': 2,
                        'reps_completed': 3,   
                    },
                ],
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token_A}",
        )
        self.assertEqual(response5_A.status_code, 200)
        response6_B = self.client.get(
            reverse('workout_session-history'),
            HTTP_AUTHORIZATION=f"Bearer {access_token_B}",
        )
        self.assertEqual(response6_B.status_code, 200)
        response6_B_json = response6_B.json()
        self.assertEqual(response6_B_json["count"], 0)
        self.assertEqual(response6_B_json['results'], [])

    def test_completed_workouts_report_counts_only_matching_sessions(self):
        user_A = MyUser.objects.create_user(
            email='razielhefer@gmail.com',
            password='wWPE4c4HJHJgXZMmhksve2pkp',
            last_name='Arik',
            first_name='Hefer',
        )
        user_B = MyUser.objects.create_user(
            email='razielhefer1@gmail.com',
            password='wWPE4234HJHJgXZMmhksve2pkp',
            last_name='Arik',
            first_name='Hefer',
        )
        response1_A = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer@gmail.com',
                'password': 'wWPE4c4HJHJgXZMmhksve2pkp',
            }
        )
        response1_B = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer1@gmail.com',
                'password': 'wWPE4234HJHJgXZMmhksve2pkp',
            }
        )
        access_token_A = response1_A.json()['access']
        access_token_B = response1_B.json()['access']
        response2_A = self.client.post(
            reverse('workout-list'),
            {
                'name': 'Chest Workout',
                'description': 'This Workout is too workout my chest'
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_A}",
        )
        response2_B = self.client.post(
            reverse('workout-list'),
            {
                'name': 'Leg Workout',
                'description': 'This Workout is too workout my chest'
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_B}",
        )
        current_time = timezone.now()
        current_date = timezone.localdate()
        past_date = timezone.now() + timedelta(days=-2)
        workout_A = Workout.objects.get(name='Chest Workout')
        workout_B = Workout.objects.get(name='Leg Workout')
        create_session1_A = WorkoutSession.objects.create(
            scheduled_at=current_time,
            status='completed',
            completed_at=current_time,
            workout=workout_A,
        )
        create_session2_A = WorkoutSession.objects.create(
            scheduled_at=current_time,
            status='completed',
            completed_at=current_time,
            workout=workout_A,
        )
        create_session3_A = WorkoutSession.objects.create(
            scheduled_at=current_time,
            status='scheduled',
            workout=workout_A,
        )
        create_session4_A = WorkoutSession.objects.create(
            scheduled_at=past_date,
            status='completed',
            completed_at=past_date,
            workout=workout_A,
        )
        create_session5_B = WorkoutSession.objects.create(
            scheduled_at=current_time,
            status='completed',
            completed_at=current_time,
            workout=workout_B,
        )
        response6 = self.client.get(
            reverse('workout_session-completed-workouts-report'),
            {
                'start_date': current_date.isoformat(),
                'end_date': current_date.isoformat(),
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_A}",
        )
        self.assertEqual(response6.status_code, 200)
        response6_json = response6.json()
        self.assertEqual(response6_json['completed_workouts'], 2)

    def test_training_volume_report_calculates_total_volume(self):
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
        exercise_create1 = Exercise.objects.create(name="Push Ups")
        exercise1 = Exercise.objects.get(name="Push Ups")
        exercise_create2 = Exercise.objects.create(name="Legs")
        exercise2 = Exercise.objects.get(name="Legs")
        workout = Workout.objects.get(user=user, name='Chest Workout')
        workout_exercise1 = WorkoutExercise.objects.create(
            order=1,
            sets=3,
            reps=2,
            rest_seconds=30,
            workout=workout,
            exercise=exercise1,
        )
        current_time = timezone.now()
        current_date = timezone.localdate()
        workout_session1 = WorkoutSession.objects.create(
            scheduled_at=current_time,
            status='completed',
            completed_at=current_time,
            workout=workout,
        )
        workout_session2 = WorkoutSession.objects.create(
            scheduled_at=current_time,
            status='completed',
            completed_at=current_time,
            workout=workout,
        )
        workout_session1_exercise_result = ExerciseResult.objects.create(
            workout_session=workout_session1,
            workout_exercise=workout_exercise1,
            sets_completed=2,
            reps_completed=5,
            weight_completed=10,
        )
        workout_session2_exercise_result = ExerciseResult.objects.create(
            workout_session=workout_session2,
            workout_exercise=workout_exercise1,
            sets_completed=3,
            reps_completed=4,
            weight_completed=20,
        )
        response3 = self.client.get(
            reverse('workout_session-training-volume-report'),
            {
                'start_date': current_date.isoformat(),
                'end_date': current_date.isoformat(),
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response3.status_code, 200)
        response3_json = response3.json()
        report_results = response3_json['results']
        self.assertEqual(len(report_results), 1)
        report_result = report_results[0]
        self.assertEqual(report_result['exercise_id'], exercise1.id)
        self.assertEqual(float(report_result['total_volume']), 340.0)

    def test_highest_weight_report_returns_maximum_weight(self):
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
        current_time = timezone.now()
        current_date = timezone.localdate()
        workout_exercise1 = WorkoutExercise.objects.create(
            order=1,
            sets=3,
            reps=2,
            rest_seconds=30,
            weight=6,
            workout=workout,
            exercise=exercise,
        )
        workout_session1 = WorkoutSession.objects.create(
            scheduled_at=current_time,
            status='completed',
            completed_at=current_time,
            workout=workout,
        )
        workout_session2 = WorkoutSession.objects.create(
            scheduled_at=current_time,
            status='completed',
            completed_at=current_time,
            workout=workout,
        )
        workout_session1_exercise_result = ExerciseResult.objects.create(
            workout_session=workout_session1,
            workout_exercise=workout_exercise1,
            sets_completed=3,
            reps_completed=4,
            weight_completed=10,
        )
        workout_session2_exercise_result = ExerciseResult.objects.create(
            workout_session=workout_session2,
            workout_exercise=workout_exercise1,
            sets_completed=3,
            reps_completed=4,
            weight_completed=20,
        )
        response3 = self.client.get(
            reverse('workout_session-highest-weight-report'),
            {
                'start_date': current_date.isoformat(),
                'end_date': current_date.isoformat(),
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response3.status_code, 200)
        response3_json = response3.json()
        report_results = response3_json['results']
        self.assertEqual(len(report_results), 1)
        report_result = report_results[0]
        self.assertEqual(report_result['exercise_id'], exercise.id)
        self.assertEqual(float(report_result['highest_weight']), 20.0)

    def test_reports_return_empty_results_when_user_has_no_data(self):
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
        current_date = timezone.localdate()
        response2 = self.client.get(
            reverse('workout_session-completed-workouts-report'),
            {
                'start_date': current_date.isoformat(),
                'end_date': current_date.isoformat(),
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response2.status_code, 200)
        response2_json = response2.json()
        self.assertEqual(response2_json['completed_workouts'], 0)
        response3 = self.client.get(
            reverse('workout_session-training-volume-report'),
            {
                'start_date': current_date.isoformat(),
                'end_date': current_date.isoformat(),
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response3.status_code, 200)
        response3_json = response3.json()
        report_results = response3_json['results']
        self.assertEqual(report_results, [])
        response4 = self.client.get(
            reverse('workout_session-highest-weight-report'),
            {
                'start_date': current_date.isoformat(),
                'end_date': current_date.isoformat(),
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response4.status_code, 200)
        response4_json = response4.json()
        report_results = response4_json['results']
        self.assertEqual(report_results, [])

    def test_report_rejects_invalid_date_range(self):
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
        current_date = timezone.localdate()
        start_date = current_date
        end_date = timezone.localdate() - timedelta(days=2)
        response2 = self.client.get(
            reverse('workout_session-completed-workouts-report'),
            {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response2.status_code, 400)

class WorkoutExerciseTests(TestCase):
    def test_update_workout_exercise_success(self):
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
        workout_exercise = WorkoutExercise.objects.get(workout=workout.id, exercise=exercise.id)
        response4 = self.client.patch(
            reverse('workout_exercise-detail', args=[workout_exercise.id]),
            {
                'sets': 6,
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response4.status_code, 200)
        workout_exercise = WorkoutExercise.objects.get(workout=workout.id, exercise=exercise.id)
        self.assertEqual(workout_exercise.sets, 6)

    def test_remove_workout_exercise_success(self):
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
        workout_exercise = WorkoutExercise.objects.get(
            exercise=exercise.id,
            workout=workout.id,
        )
        response4 = self.client.delete(
            reverse('workout_exercise-detail', args=[workout_exercise.id]),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response4.status_code, 204)
        self.assertEqual(WorkoutExercise.objects.count(), 0)

    def test_cannot_add_workout_exercise_with_zero_sets(self):
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
                'sets': 0,
                'reps': 3,
                'rest_seconds': 30,
                'workout': workout.id,
                'exercise': exercise.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response3.status_code, 400)
        self.assertEqual(WorkoutExercise.objects.count(), 0)

    def test_cannot_add_workout_exercise_with_negative_weight(self):
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
                'sets': 4,
                'reps': 3,
                'rest_seconds': 30,
                'weight': -2,
                'workout': workout.id,
                'exercise': exercise.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response3.status_code, 400)
        self.assertEqual(WorkoutExercise.objects.count(), 0)

    def test_user_cannot_update_other_users_workout_exercise(self):
        user_A = MyUser.objects.create_user(
            email='razielhefer1@gmail.com',
            password='wWPE4c4H66HJgXZMmhksve2pkp',
            last_name='Raziel',
            first_name='Hefer',
        )
        user_B = MyUser.objects.create_user(
            email='razielhefer@gmail.com',
            password='wWPE4c4HJHJgXZMmhksve2pkp',
            last_name='Arik',
            first_name='Hefer',
        )
        response1_A = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer1@gmail.com',
                'password': 'wWPE4c4H66HJgXZMmhksve2pkp',
            }
        )
        response1_B = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer@gmail.com',
                'password': 'wWPE4c4HJHJgXZMmhksve2pkp',
            }
        )   
        access_token_A = response1_A.json()['access']
        access_token_B = response1_B.json()['access']
        response2_A = self.client.post(
            reverse('workout-list'),
            {
                'name': 'Chest Workout',
                'description': 'This Workout is too workout my chest'
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_A}",
        )
        exercise_create = Exercise.objects.create(name="Push Ups")
        exercise = Exercise.objects.get(name="Push Ups")
        workout = Workout.objects.get(user=user_A, name='Chest Workout')
        response3_A = self.client.post(
            reverse('workout_exercise-list'),
            {
                'order': 1,
                'sets': 4,
                'reps': 3,
                'rest_seconds': 30,
                'weight': 2,
                'workout': workout.id,
                'exercise': exercise.id,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_A}",
        )
        workout_exercise = WorkoutExercise.objects.get(workout=workout.id, exercise=exercise.id)
        response4_B = self.client.patch(
            reverse('workout_exercise-detail', args=[workout_exercise.id]),
            {
                'sets': 2,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token_B}",
        )
        self.assertEqual(response4_B.status_code, 404)
        updated_workout_exercise = WorkoutExercise.objects.get(workout=workout.id, exercise=exercise.id)
        self.assertEqual(updated_workout_exercise.sets, 4)

