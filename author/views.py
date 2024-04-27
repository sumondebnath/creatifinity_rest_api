from django.shortcuts import render,redirect
from rest_framework import viewsets, filters, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from author.models import UserAccount, UserAddress
from author.serializers import UserAddressSerializers, UserRegistrationSerializers, UserLoginSerializers, UserAccountSerializers 
    # registration and token uid
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
    #email sendig
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.

class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializers
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializers
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class UserRegistrationViewSet(APIView):
    serializer_class = UserRegistrationSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print("user:", user)
            token =default_token_generator.make_token(user)
            print("token: ",token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)

            # confirm_link = f"http://127.0.0.1:8000/active/{uid}/{token}"
            confirm_link = f"https://creatifinity-api.onrender.com/account/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string("confirm_email.html", {"confirm_link":confirm_link})
            email = EmailMultiAlternatives(email_subject, "", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check Your Email for Confirmation.")
        return Response(serializer.errors)
    

def Active(request, uid64, token):
    print("hi")
    try:
        print("hey")
        uid = urlsafe_base64_decode(uid64).decode()
        print(uid)
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        return redirect("register")
    

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializers(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)

            if user:
                token, other = Token.objects.get_or_create(user=user)
                print(token, other)
                login(request, user)
                return Response({"token":token.key, "user_id":user.id})
            else:
                return Response({"error":"Invalid Credential"})
        return Response(serializer.errors)
    

class UserLogoutView(APIView):
    # def get(self, request):
    #     request.user.auth_token.delete()
    #     logout(request)
    #     return redirect("login")

    def post(self, request):
        try:
            token_key = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
            token = Token.objects.get(key = token_key)
            token.delete()
            return Response({"message":"Logout Successfully."})
        except Token.DoesNotExist:
            return Response({"error":"Invalid Token"})
        except AttributeError:
            return Response({'error': 'Token not provided'})