from django.shortcuts import render
from .models import Projects, Issues, Comments
from .serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status


# Create your views here.


class ViewSetProjects(APIView):
    """Acces API Control Projects"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Projects.objects.filter(Q(author=self.request.user) | Q(contributor=self.request.user))
        serializer = ProjectsSerializer(projects, many=True)

    def post(self, request):
        request.data["author"] = self.request.user
        print(request.data)
        serializer = ProjectsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
