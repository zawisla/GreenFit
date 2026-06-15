from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegistrationTests(TestCase):
    def test_registration_creates_user_and_logs_in(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "greenuser",
            "email": "green@example.com",
            "password1": "Sansevieria42",
            "password2": "Sansevieria42",
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="greenuser")
        self.assertEqual(user.email, "green@example.com")
        # The new user is authenticated immediately after registering.
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_passwords_must_match(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "mismatch",
            "email": "m@example.com",
            "password1": "Sansevieria42",
            "password2": "Different99",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="mismatch").exists())


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="leaf", password="Monstera123")

    def test_login_succeeds(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "leaf",
            "password": "Monstera123",
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_requires_post(self):
        # GET must not log the user out (logout is POST-only in Django 5).
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
