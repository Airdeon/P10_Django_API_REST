from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("id", "username", "email", "profile", "password")

    def create(self, validated_data):
        return User.objects.create(request_data=validated_data)
