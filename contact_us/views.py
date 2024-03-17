from django.shortcuts import render
from rest_framework import viewsets
from contact_us.models import ContactUs
from contact_us.serializers import ContactUsSerializers

# Create your views here.

class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializers