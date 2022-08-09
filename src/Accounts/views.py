from django.shortcuts import render
from rest_framework import authentication, permissions, status, viewsets, filters
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.db import transaction
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from API.models import Projects

# Create your views here.


class Signup(CreateAPIView):
    serializer_class = UserSerializer


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self, pk):
        return Projects.objects.filter(id=pk).contributor
