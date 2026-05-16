import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creatifinity_blog.settings')
django.setup()

from author.serializers import UserRegistrationSerializers

data = {
    "username": "test_user_for_email",
    "first_name": "Test",
    "last_name": "User",
    "email": "test_user_for_email@example.com",
    "password": "TestPass123",
    "confirm_password": "TestPass123",
}

serializer = UserRegistrationSerializers(data=data)
if serializer.is_valid():
    user = serializer.save()
    print("Created user:", user.username, "id:", user.id)
else:
    print("Serializer errors:", serializer.errors)
