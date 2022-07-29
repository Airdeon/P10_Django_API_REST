from django.shortcuts import render
from rest_framework import authentication, permissions, generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from django.db import transaction
from .serializers import UserSerializer

# Create your views here.


class Register(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @transaction.atomic
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
