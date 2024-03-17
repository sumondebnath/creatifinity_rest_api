from django.urls import path, include
from rest_framework.routers import DefaultRouter
from author.views import UserAddressViewSet, UserRegistrationViewSet, Active, UserLoginView, UserLogoutView, UserAccountViewSet


router = DefaultRouter()

router.register("account", UserAccountViewSet)
router.register("address", UserAddressViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationViewSet.as_view(), name="register"),
    path("active/<uid64>/<token>/", Active, name="active"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]