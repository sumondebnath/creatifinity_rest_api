from django.urls import path, include
from rest_framework.routers import DefaultRouter
from contact_us.views import ContactUsViewSet


router = DefaultRouter()

router.register("list", ContactUsViewSet)


urlpatterns = [
    path("", include(router.urls)),
]