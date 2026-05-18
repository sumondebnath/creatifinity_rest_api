from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from category.models import Category


class CategoryTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user1", email="user1@example.com", password="pass1234")
        self.category = Category.objects.create(name="Test Category", slug="test-category")

    def test_list_categories(self):
        response = self.client.get("/category/list/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["slug"], self.category.slug)

    def test_create_category_requires_authentication(self):
        response = self.client.post(
            "/category/list/",
            {"name": "New Category", "slug": "new-category"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/category/list/",
            {"name": "New Category", "slug": "new-category"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_retrieve_category(self):
        response = self.client.get(f"/category/list/{self.category.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.category.name)

    def test_update_category_requires_authentication(self):
        response = self.client.patch(
            f"/category/list/{self.category.id}/",
            {"name": "Updated Name"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/category/list/{self.category.id}/",
            {"name": "Updated Name"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Updated Name")

    def test_delete_category_requires_authentication(self):
        response = self.client.delete(f"/category/list/{self.category.id}/")
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/category/list/{self.category.id}/")
        self.assertEqual(response.status_code, 204)
