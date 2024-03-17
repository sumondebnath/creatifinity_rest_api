from django.db import models
from django.contrib.auth.models import User
from author.constants import GENDER_TYPE

# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="author/images/", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField()


class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)