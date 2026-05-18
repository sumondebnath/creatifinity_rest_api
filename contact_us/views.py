from rest_framework import viewsets, permissions
from contact_us.models import ContactUs
from contact_us.serializers import ContactUsSerializers

# Create your views here.

class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializers

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(status="new")