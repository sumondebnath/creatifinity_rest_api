from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .serializers import UserSerializers
from rest_framework import viewsets, permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]