from django.shortcuts import render
from rest_framework import authentication, permissions, status, viewsets, filters
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.db import transaction
from .serializers import UserSerializer

# Create your views here.


class Signup(CreateAPIView):
    serializer_class = UserSerializer
