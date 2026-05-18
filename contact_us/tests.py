from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from contact_us.models import ContactUs


class ContactUsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username="admin", email="admin@example.com", password="pass1234", is_staff=True)
        self.user = User.objects.create_user(username="user", email="user@example.com", password="pass1234")

    def test_create_contact_message_allows_anonymous(self):
        response = self.client.post(
            "/contact_us/list/",
            {"name": "Test User", "email": "test@example.com", "body": "Hello"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Test User")
        self.assertEqual(response.data["status"], "new")

    def test_list_contact_messages_requires_admin(self):
        response = self.client.get("/contact_us/list/")
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.user)
        response = self.client.get("/contact_us/list/")
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/contact_us/list/")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_contact_message_requires_admin(self):
        contact = ContactUs.objects.create(name="Test User", email="test@example.com", body="Hello")
        response = self.client.get(f"/contact_us/list/{contact.id}/")
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/contact_us/list/{contact.id}/")
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"/contact_us/list/{contact.id}/")
        self.assertEqual(response.status_code, 200)

    def test_update_contact_message_requires_admin(self):
        contact = ContactUs.objects.create(name="Test User", email="test@example.com", body="Hello")
        response = self.client.patch(
            f"/contact_us/list/{contact.id}/",
            {"status": "open"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/contact_us/list/{contact.id}/",
            {"status": "open"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f"/contact_us/list/{contact.id}/",
            {"status": "open"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "open")

    def test_delete_contact_message_requires_admin(self):
        contact = ContactUs.objects.create(name="Test User", email="test@example.com", body="Hello")
        response = self.client.delete(f"/contact_us/list/{contact.id}/")
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/contact_us/list/{contact.id}/")
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/contact_us/list/{contact.id}/")
        self.assertEqual(response.status_code, 204)
