from rest_framework import serializers
from contact_us.models import ContactUs


class ContactUsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ["id", "name", "email", "body", "status", "created"]
        read_only_fields = ["created"]