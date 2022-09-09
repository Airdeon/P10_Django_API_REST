import re
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Projects, Issues, Comments
from .serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer, ContributorSerializer
from .permissions import ProjectPermission, IssuePermission, CommentPermission

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class ProjectsViewSet(ModelViewSet):

    serializer_class = ProjectsSerializer
    permission_classes = (ProjectPermission,)

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


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = (ProjectPermission,)

    def get_queryset(self):
        print(self.kwargs)

        if "pk" in self.kwargs:
            print(int(self.kwargs["pk"]))
            return Projects.objects.filter(id=int(self.kwargs["pk"]))
        else:
            print(self.request.user)
            return Projects.objects.filter(Q(author=self.request.user) | Q(contributor__in=[self.request.user]))

    def create(self, request, *args, **kwargs):
        data = request.data
        project = Projects.objects.get(id=self.kwargs["projects_pk"])
        project.contributor.add(User.objects.get(username=data["username"]))
        print("ModelViewSet")
        print(data)
        serializer = ContributorSerializer(project)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        data = request.data
        project = Projects.objects.get(id=self.kwargs["projects_pk"])
        project.contributor.remove(User.objects.get(username=data["username"]))
        print("ModelViewSet")
        print(data)
        serializer = ContributorSerializer(project)
        return Response(serializer.data)


class IssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = (IssuePermission,)

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
    permission_classes = (CommentPermission,)

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
