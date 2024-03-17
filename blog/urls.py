from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import BlogViewSet, ReviewViewSet

router = DefaultRouter()

router.register("list", BlogViewSet)
router.register("review", ReviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
]