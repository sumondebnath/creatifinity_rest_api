from django.shortcuts import render
from blog.serializers import BlogSerializers, ReviewSerializers
from blog.models import Blog, Review
from rest_framework import viewsets, filters, pagination

# Create your views here.

class BlogPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = page_size
    max_page_size = 100

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers
    filter_backends = [filters.SearchFilter]
    pagination_class = BlogPagination
    search_fields = ["user__first_name", "blog__category", "blog__title"]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers