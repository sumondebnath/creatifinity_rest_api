import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creatifinity_blog.settings')
django.setup()

from django.test import Client

c = Client()
resp = c.post('/account/token/', json.dumps({'username':'test_user_for_email','password':'TestPass123'}), content_type='application/json')
print('status code:', resp.status_code)
try:
    print('response:', resp.json())
except Exception:
    print('response content:', resp.content)
