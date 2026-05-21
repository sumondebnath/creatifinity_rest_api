from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from author.models import UserAccount, UserAddress
from author.serializers import UserAddressSerializers, UserRegistrationSerializers, UserAccountSerializers
from author.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            base_url = getattr(settings, "BASE_URL", "https://creatifinity-rest-api.vercel.app/")
            confirm_link = f"{base_url}/account/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string("confirm_email.html", {"confirm_link": confirm_link})
            email_plain_text = f"Click the link to confirm your email: {confirm_link}"
            email = EmailMultiAlternatives(email_subject, email_plain_text, to=[user.email])
            email.attach_alternative(email_body, "text/html")
            try:
                email.send()
                return Response({"detail": "Check your email for confirmation."}, status=201)
            except Exception as e:
                return Response({"detail": f"Failed to send confirmation email: {str(e)}"}, status=500)
        return Response(serializer.errors, status=400)
    

def Active(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Redirect to login page after successful activation
        return redirect('/account/login/')
    # Redirect to register page on failure
    return redirect('/account/register/')


class LoginView(TokenObtainPairView):
    """Handles JWT login at /account/login/."""

    def get(self, request, *args, **kwargs):
        msg = (
            'Your account has been activated. To obtain JWT tokens, POST your username and password '
            'to /account/login/ (JSON body: {"username":..., "password":...}).'
        )
        return HttpResponse(msg)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"refresh": "This field is required."}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid or expired refresh token."}, status=400)

        return Response({"detail": "Logout successful."})