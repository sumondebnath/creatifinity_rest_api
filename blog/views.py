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
    search_fields = ["user__username", "user__first_name", "user__last_name", "category__name", "title"]

    def get_queryset(self):
        queryset = super().get_queryset()
        # account_id = self.request.query_params.get('account_id')
        user_id = self.request.query_params.get("user_id")
        # print(account_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers