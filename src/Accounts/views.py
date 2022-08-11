from django.shortcuts import render
from rest_framework import authentication, permissions, status, viewsets, filters
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.db import transaction
from .serializers import ProjectUserSerializer, UserSignupSerializer
from rest_framework.viewsets import ModelViewSet
from API.models import Projects
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class Signup(CreateAPIView):
    serializer_class = UserSignupSerializer


class UserViewSet(ModelViewSet):

    serializer_class = ProjectUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(Projects.objects.get(id=self.kwargs["projects_pk"]).contributor)
        return Projects.objects.get(id=self.kwargs["projects_pk"]).contributor

    def create(self, request, *args, **kwargs):
        data = request.data
        project = Projects.objects.get(id=self.kwargs["projects_pk"])
        project.contributor.add(User.objects.get(username=data["username"]))
        print("ModelViewSet")
        print(data)
        serializer = ProjectUserSerializer(project)
        return Response(serializer.data)
