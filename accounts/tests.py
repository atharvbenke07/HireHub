from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Profile


class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Test@123"
        )

        Profile.objects.create(
            user=self.user,
            user_type="job_seeker"
        )

    def test_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "Test@123",
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(
            username="testuser",
            password="Test@123"
        )

        response = self.client.get(
            reverse("logout")
        )

        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_login(self):
        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(response.status_code, 302)