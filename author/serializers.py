from rest_framework import serializers
from author.models import UserAccount, UserAddress
from django.contrib.auth.models import User


class UserAccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
        }


class UserAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
        }



class UserRegistrationSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user


class UserLoginSerializers(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})




# class UserEditProfileSerializers(serializers.ModelSerializer):
#     image = serializers.ImageField(up)