from django.urls import path, include
from rest_framework.routers import DefaultRouter
from author.views import UserAddressViewSet, UserRegistrationView, Active, UserAccountViewSet, LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()

router.register("account", UserAccountViewSet)
router.register("address", UserAddressViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("active/<uid64>/<token>/", Active, name="active"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
