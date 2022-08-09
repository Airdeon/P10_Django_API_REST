import re
from django.shortcuts import render
from .models import Projects, Issues, Comments
from .serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer

from rest_framework.viewsets import ModelViewSet

from django.db.models import Q


# Create your views here.
class ProjectsViewSet(ModelViewSet):

    serializer_class = ProjectsSerializer

    def get_queryset(self):
        return Projects.objects.filter(Q(author=self.request.user) | Q(contributor=self.request.user))

    def get_serializer_context(self):
        context = super(ProjectsViewSet, self).get_serializer_context()
        context.update({"author": self.request.user})
        return context
