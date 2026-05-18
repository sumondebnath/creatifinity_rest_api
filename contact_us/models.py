from django.db import models

# Create your models here.

class ContactUs(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("open", "Open"),
        ("closed", "Closed"),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Contact Us"