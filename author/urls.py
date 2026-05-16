from django.urls import path, include
from rest_framework.routers import DefaultRouter
from author.views import UserAddressViewSet, UserRegistrationView, Active, UserAccountViewSet, LoginInfo
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()

router.register("account", UserAccountViewSet)
router.register("address", UserAddressViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("active/<uid64>/<token>/", Active, name="active"),
    path("login/", LoginInfo, name="login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
