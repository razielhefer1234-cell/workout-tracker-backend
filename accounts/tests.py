from django.test import TestCase
from .models import MyUser
from django.urls import reverse


class MyUserTests(TestCase):
    def test_sign_up(self):
        response = self.client.post(
            reverse('sign_up'),
            {
                'email': 'razielhefer@gmail.com',
                'password': 'wWPE4c4HJHJgXZMmhx4EXpkp',
                'first_name': 'Raziel',
                'last_name': 'Hefer',
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(MyUser.objects.count(), 1)
        user = MyUser.objects.get(email='razielhefer@gmail.com')
        self.assertTrue(user.check_password('wWPE4c4HJHJgXZMmhx4EXpkp'))
        self.assertNotIn("password", response.json())

    def test_duplicate_registration(self):
        response1 = self.client.post(
            reverse('sign_up'),
            {
                'email': 'razielhefer@gmail.com',
                'password': 'wWPE4c4HJHJgXZMmhx4EXpkp',
                'first_name': 'Raziel',
                'last_name': 'Hefer',
            }
        )
        self.assertEqual(response1.status_code, 201)
        
        response2 = self.client.post(
            reverse('sign_up'),
            {
                'email': 'razielhefer@gmail.com',
                'password': 'wWPE4c4HJHJgXZMmhksve2pkp',
                'first_name': 'Arik',
                'last_name': 'Hefer',
            }
        )
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(MyUser.objects.count(), 1)

    def test_login(self):
        user = MyUser.objects.create_user(
            email='razielhefer@gmail.com',
            password='wWPE4c4HJHJgXZMmhksve2pkp',
            last_name='Arik',
            first_name='Hefer',
        )
        response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer@gmail.com',
                'password': 'wWPE4c4HJHJgXZMmhksve2pkp',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_login_rejects_incorrect_password(self):
        user = MyUser.objects.create_user(
            email='razielhefer@gmail.com',
            password='wWPE4c4HJHJgXZMmhksve2pkp',
            last_name='Arik',
            first_name='Hefer',
        )
        response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'razielhefer@gmail.com',
                'password': 'wWPd7c4HJHJgXZMmhksve2pkp',
            }
        )
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("access", response.json())
        self.assertNotIn("refresh", response.json())

    def test_refresh_returns_access_token(self): 
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
        self.assertEqual(response1.status_code, 200)
        refresh_token = response1.json()["refresh"]
        response2 = self.client.post(
            reverse('token_refresh'),
            {
                'refresh': refresh_token,
            }
        )
        self.assertEqual(response2.status_code, 200)
        self.assertIn("access", response2.json())

    def test_logout_blacklists_refresh_token(self):
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
        refresh_token = response1.json()["refresh"]
        access_token = response1.json()["access"]
        response2 = self.client.post(
            reverse('logout'),
            {
                'refresh': refresh_token,
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response2.status_code, 200)
        response2 = self.client.post(
            reverse('token_refresh'),
            {
                'refresh': refresh_token,
            }
        )
        self.assertEqual(response2.status_code, 401)
        self.assertNotIn("refresh", response2.json())

    def test_current_user_returns_authenticated_user(self):
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
        access_token = response1.json()["access"]
        response2 = self.client.get(
            reverse('user_info'),
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response2.status_code, 200)
        self.assertIn("email", response2.json())
        self.assertIn("id", response2.json())

    def test_current_user_requires_authentication(self):
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
        access_token = response1.json()["access"]
        response2 = self.client.get(
            reverse('user_info'),
        )
        self.assertEqual(response2.status_code, 401)