from rest_framework.permissions import BasePermission


class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return True
        elif request.method == "GET":
            return bool(obj.author == request.user or request.user in obj.contributor)
        elif request.method == "PUT" or request.method == "DELETE":
            return bool(obj.author == request.user)
        else:
            False


class IssuePermission(BasePermission):
    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return bool(obj.project.author == request.user or request.user in obj.project.contributor)
        elif request.method == "GET":
            return bool(obj.author == request.user or request.user in obj.project.contributor)
        elif request.method == "PUT" or request.method == "DELETE":
            return bool(obj.author == request.user)
        else:
            False


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return bool(obj.issue.project.author == request.user or request.user in obj.issue.project.contributor)
        elif request.method == "GET":
            return bool(obj.author == request.user or request.user in obj.issue.project.contributor)
        elif request.method == "PUT" or request.method == "DELETE":
            return bool(obj.author == request.user)
        else:
            False
