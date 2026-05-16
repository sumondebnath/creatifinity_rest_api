import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creatifinity_blog.settings')
django.setup()

from django.contrib.auth.models import User

username = 'test_user_for_email'
try:
    u = User.objects.get(username=username)
    u.is_active = True
    u.save()
    print('Activated user', username)
except User.DoesNotExist:
    print('User not found:', username)
