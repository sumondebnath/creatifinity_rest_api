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

            # confirm_link = f"https://creatifinity-api.onrender.com/account/active/{uid}/{token}"
            confirm_link = f"http://127.0.0.1:8000/account/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string("confirm_email.html", {"confirm_link": confirm_link})
            email_plain_text = f"Click the link to confirm your email: {confirm_link}"
            email = EmailMultiAlternatives(email_subject, email_plain_text, to=[user.email])
            email.attach_alternative(email_body, "text/html")
            try:
                email.send()
                return Response({"detail": "Check your email for confirmation."})
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


def LoginInfo(request):
    """Simple informational page informing user how to login (token endpoint)."""
    msg = (
        "Your account has been activated. To obtain JWT tokens, POST your username and password "
        "to /account/token/ (JSON body: {\"username\":..., \"password\":...})."
    )
    return HttpResponse(msg)
    

"""Login and logout are handled via JWT token endpoints."""