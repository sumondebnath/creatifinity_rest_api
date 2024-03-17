from django.db import models
from django.contrib.auth.models import User
from category.models import Category
from blog.constants import RATINGS

# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to="blog/images/")
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    rating = models.CharField(max_length=10, choices=RATINGS)

    def __str__(self):
        return f"{self.user.first_name} {self.user.first_name} {self.rating}"