import re
from django.shortcuts import render
from .models import Projects, Issues, Comments
from .serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class ProjectsViewSet(ModelViewSet):

    serializer_class = ProjectsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(self.kwargs)

        if "pk" in self.kwargs:
            print(int(self.kwargs["pk"]))
            return Projects.objects.filter(id=int(self.kwargs["pk"]))
        else:
            print(self.request.user)
            return Projects.objects.filter(Q(author=self.request.user) | Q(contributor__in=[self.request.user]))

    def get_serializer_context(self):
        context = super(ProjectsViewSet, self).get_serializer_context()
        context.update({"author": self.request.user})
        return context


class IssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(self.kwargs)

        if "pk" in self.kwargs:
            print(int(self.kwargs["pk"]))
            return Issues.objects.filter(id=int(self.kwargs["pk"]))
        else:
            print(self.request.user)
            return Issues.objects.filter(project=Projects.objects.get(id=int(self.kwargs["projects_pk"])))

    def get_serializer_context(self):
        context = super(IssuesViewSet, self).get_serializer_context()
        context.update({"author": self.request.user})
        context.update({"project": Projects.objects.get(id=int(self.kwargs["projects_pk"]))})
        return context


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(self.kwargs)

        if "pk" in self.kwargs:
            print(int(self.kwargs["pk"]))
            return Comments.objects.filter(id=int(self.kwargs["pk"]))
        else:
            print(self.request.user)
            return Comments.objects.filter(issue=Issues.objects.get(id=int(self.kwargs["issues_pk"])))

    def get_serializer_context(self):
        context = super(CommentsViewSet, self).get_serializer_context()
        context.update({"issue": Issues.objects.get(id=int(self.kwargs["issues_pk"]))})
        context.update({"author": self.request.user})
        return context
