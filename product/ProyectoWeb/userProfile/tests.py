from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
            first_name="Test",
            last_name="User"
        )
        self.client.login(username="testuser", password="testpassword123")

    def test_view_profile_details(self):
        # Test GET request to view profile details
        response = self.client.get(reverse('detalle_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userProfile/detalle_profile.html')
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)

    def test_update_profile_valid(self):
        # Test POST request with valid data to update profile
        data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "Name",
            "password1": "",
            "password2": ""
        }
        response = self.client.post(reverse('detalle_profile'), data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful update
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.email, "updateduser@example.com")
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")

    def test_update_profile_invalid_passwords(self):
        # Test POST request with non-matching passwords
        data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "Name",
            "password1": "newpassword123",
            "password2": "differentpassword"
        }
        response = self.client.post(reverse('detalle_profile'), data)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertContains(response, "Las contraseñas no coinciden.")

    def test_delete_account(self):
        # Test DELETE account functionality
        response = self.client.get(reverse('eliminar_cuenta'))
        self.assertEqual(response.status_code, 302)  # Should redirect after deletion
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="testuser")  # User should no longer exist
