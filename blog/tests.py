from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from blog.models import Blog, Review
from category.models import Category


class BlogAppTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="user1", email="user1@example.com", password="pass1234")
        self.user2 = User.objects.create_user(username="user2", email="user2@example.com", password="pass1234")
        self.category = Category.objects.create(name="TestCategory", slug="test-category")

    def test_blog_create_sets_user_and_ignores_payload_user(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            "/blog/list/",
            {
                "title": "New Blog",
                "body": "Blog body text.",
                "user": self.user2.id,
                "category": [self.category.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"], self.user1.id)
        self.assertEqual(response.data["title"], "New Blog")
        self.assertEqual(response.data["category"], [self.category.id])

    def test_blog_create_allows_empty_category(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            "/blog/list/",
            {
                "title": "No Category Blog",
                "body": "Body with no category.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"], self.user1.id)
        self.assertEqual(response.data.get("category"), [])

    def test_blog_owner_only_can_update(self):
        blog = Blog.objects.create(user=self.user1, title="Owner Blog", body="Body")
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(
            f"/blog/list/{blog.id}/",
            {"title": "Hacked Title"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_blog_pagination_uses_page_size_query_param(self):
        self.client.force_authenticate(user=self.user1)
        for idx in range(3):
            Blog.objects.create(user=self.user1, title=f"Blog {idx}", body="Body")
        response = self.client.get("/blog/list/?page_size=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertIsNotNone(response.data.get("next"))

    def test_review_create_sets_user_and_ignores_payload_user(self):
        blog = Blog.objects.create(user=self.user1, title="Review Blog", body="Body")
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            "/blog/review/",
            {
                "blog": blog.id,
                "rating": 5,
                "user": self.user2.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"], self.user1.id)
        self.assertEqual(response.data["blog"], blog.id)

    def test_review_owner_only_can_delete(self):
        blog = Blog.objects.create(user=self.user1, title="Review Blog", body="Body")
        review = Review.objects.create(user=self.user1, blog=blog, rating=5)
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f"/blog/review/{review.id}/")
        self.assertEqual(response.status_code, 403)
