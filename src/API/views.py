from django.contrib.auth.models import User
from .models import Projects, Issues, Comments
from .serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer, ContributorSerializer
from .permissions import ProjectPermission, IssuePermission, CommentPermission, ProjectUserPermission
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework.response import Response
from django.http import Http404


# Create your views here.
class ProjectsViewSet(ModelViewSet):

    serializer_class = ProjectsSerializer
    permission_classes = (ProjectPermission,)

    def get_queryset(self):
        if "pk" in self.kwargs:
            try:
                project = Projects.objects.filter(id=int(self.kwargs["pk"]))
                return project
            except ValueError:
                raise Http404("Numéro de projet invalide")
        else:
            projects = Projects.objects.filter(Q(author=self.request.user) | Q(contributor=self.request.user))
            list_project = []
            for project in projects:
                if project not in list_project:
                    list_project.append(project)
            return list_project

    def get_serializer_context(self):
        context = super(ProjectsViewSet, self).get_serializer_context()
        context.update({"author": self.request.user})
        return context


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = (ProjectUserPermission,)

    def get_queryset(self):
        try:
            project = Projects.objects.filter(id=int(self.kwargs["projects_pk"]))
            return project
        except ValueError:
            raise Http404("Numéro de projet invalide")

    def create(self, request, *args, **kwargs):
        """Add user to a project (new contributor)"""
        data = request.data
        project = Projects.objects.get(id=self.kwargs["projects_pk"])
        self.check_object_permissions(self.request, project)
        project.contributor.add(User.objects.get(username=data["username"]))
        serializer = ContributorSerializer(project)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Remove user from project (remove contributor)"""
        user = User.objects.get(id=self.kwargs["pk"])
        project = Projects.objects.get(id=self.kwargs["projects_pk"])
        self.check_object_permissions(self.request, project)
        project.contributor.remove(user)
        serializer = ContributorSerializer(project)
        return Response(serializer.data)


class IssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = (IssuePermission,)

    def get_queryset(self):
        if "pk" in self.kwargs:
            return Issues.objects.filter(id=int(self.kwargs["pk"]))
        else:
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
        if "pk" in self.kwargs:
            return Comments.objects.filter(id=int(self.kwargs["pk"]))
        else:
            return Comments.objects.filter(issue=Issues.objects.get(id=self.kwargs["issues_pk"]))

    def get_serializer_context(self):
        context = super(CommentsViewSet, self).get_serializer_context()
        context.update({"issue": Issues.objects.get(id=int(self.kwargs["issues_pk"]))})
        context.update({"author": self.request.user})
        return context
