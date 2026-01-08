from rest_framework import serializers
from author.models import UserAccount, UserAddress
from django.contrib.auth.models import User


class UserAccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"


class UserAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"



class UserRegistrationSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "confirm_password"]

    def save(self):
        username = self.validated_data["username"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        email = self.validated_data["email"]
        password = self.validated_data["password"]
        password2 = self.validated_data["confirm_password"]

        if password != password2:
            raise serializers.ValidationError({"error":"Password Does Not Matched."})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error":"Email Already Exists."})
        
        account = User(username=username, first_name=first_name, last_name=last_name, email=email)
        account.set_password(password)
        # account.is_active = False
        account.is_active = True
        account.save()
        return account
    

class UserLoginSerializers(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)




# class UserEditProfileSerializers(serializers.ModelSerializer):
#     image = serializers.ImageField(up)