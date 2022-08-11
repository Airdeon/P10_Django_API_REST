import re
from django.shortcuts import render
from .models import Projects, Issues, Comments
from .serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q


# Create your views here.
class ProjectsViewSet(ModelViewSet):

    serializer_class = ProjectsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(self.kwargs)
        if "pk" in self.kwargs:
            return Projects.objects.filter(id=self.kwargs["pk"])
        else:
            print(self.request.user)
            return Projects.objects.filter(Q(author=self.request.user) | Q(contributor__in=[self.request.user]))

    def get_serializer_context(self):
        context = super(ProjectsViewSet, self).get_serializer_context()
        context.update({"author": self.request.user})
        return context
