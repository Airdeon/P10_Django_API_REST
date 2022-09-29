from rest_framework.permissions import BasePermission
from API.models import Projects, Issues
from django.http import Http404


class ProjectPermission(BasePermission):
    message = "Vous n'avez pas les droits pour cela !"

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs authentifiés
        print("has_perm")
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        print("obj perm")
        # permet la creation de projets a tous utilisateur authentifiés
        if request.method == "POST":
            return True

        # Permet a tous contributeur ou autheur de voir leur projets
        elif request.method == "GET":
            print("get")
            print(obj.contributor)
            return bool(obj.author == request.user or request.user in obj.contributor.all())

        # Authorise la modification et la suppression qu'au autheur du project
        elif request.method == "PUT" or request.method == "DELETE":
            return bool(obj.author == request.user)

        else:
            return False


class ProjectUserPermission(BasePermission):
    message = "Vous n'avez pas les droits pour cela !"

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs authentifiés autheur ou contributeur du projet
        print("has_perm")
        try:
            project = Projects.objects.get(id=view.kwargs["projects_pk"])
        except Projects.DoesNotExist:
            raise Http404("Projet introuvable")
        if request.user and request.user.is_authenticated:
            if request.user == project.author or request.user in project.contributor.all():
                return True
        return False

    def has_object_permission(self, request, view, obj):
        print("obj perm")
        if request.method == "GET":
            print("get")
            return True
        elif request.method in ["POST", "PUT", "DELETE"]:
            print("post")
            return bool(obj.author == request.user)
        else:
            return False


class IssuePermission(BasePermission):
    message = "Vous n'avez pas les droits pour cela !"

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs authentifiés auteur ou contributeur du projet
        try:
            project = Projects.objects.get(id=view.kwargs["projects_pk"])
        except Projects.DoesNotExist:
            raise Http404("Projet introuvable")
        if request.user and request.user.is_authenticated:
            if request.user == project.author or request.user in project.contributor.all():
                return True
        return False

    def has_object_permission(self, request, view, obj):
        print(obj.project.contributor.all())
        if request.method == "POST":
            return bool(obj.project.author == request.user or request.user in obj.project.contributor.all())
        elif request.method == "GET":
            return bool(obj.author == request.user or request.user in obj.project.contributor.all())
        elif request.method == "PUT" or request.method == "DELETE":
            return bool(obj.author == request.user)
        else:
            False


class CommentPermission(BasePermission):
    message = "Vous n'avez pas les droits pour cela !"

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs authentifiés auteur ou contributeur du projet
        try:
            project = Projects.objects.get(id=view.kwargs["projects_pk"])

        except Projects.DoesNotExist:
            raise Http404("Introuvable")
        try:
            Issues.objects.get(id=view.kwargs["issues_pk"])
        except Issues.DoesNotExist:
            raise Http404("Introuvable")

        if request.user and request.user.is_authenticated:
            if request.user == project.author or request.user in project.contributor.all():
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return bool(obj.issue.project.author == request.user or request.user in obj.issue.project.contributor.all())
        elif request.method == "GET":
            return bool(obj.author == request.user or request.user in obj.issue.project.contributor.all())
        elif request.method == "PUT" or request.method == "DELETE":
            return bool(obj.author == request.user)
        else:
            False
