from django.shortcuts import render
from rest_framework import viewsets, permissions
from category.models import Category
from category.serializers import CategorySerializers

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    # permission_classes = [permissions.IsAuthenticated]