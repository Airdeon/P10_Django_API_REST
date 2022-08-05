from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")

    def validate_password(self, value):
        if len(value) > 4:
            return make_password(value)
        else:
            raise serializers.ValidationError("Mot de passe trop court, minimum 5 caractères")
