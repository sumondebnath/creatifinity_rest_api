from django.urls import path, include
from rest_framework.routers import DefaultRouter
from category.views import CategoryViewSet

router = DefaultRouter()

router.register("list", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]