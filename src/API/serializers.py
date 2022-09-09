from rest_framework import serializers
from .models import Projects, Issues, Comments
from Accounts.serializers import ProjectUserSerializer
from django.contrib.auth.models import User


class ProjectsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    contributor = serializers.StringRelatedField(many=True)

    class Meta:
        model = Projects
        fields = [
            "id",
            "title",
            "description",
            "type",
            "author",
            "contributor",
        ]

    def validate(self, data, **kwargs):
        data["author"] = self.context["author"]
        return data


class ContributorSerializer(serializers.ModelSerializer):
    contributor = serializers.StringRelatedField(many=True)

    class Meta:
        model = Projects
        fields = ("contributor",)


class IssuesSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    contributor = serializers.StringRelatedField(many=True)

    class Meta:
        model = Issues
        fields = [
            "id",
            "project",
            "author",
            "contributor",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "created_time",
        ]

    def validate(self, data, **kwargs):
        data["project"] = self.context["project"]
        data["author"] = self.context["author"]
        return data


class CommentsSerializer(serializers.ModelSerializer):
    issue = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Comments
        fields = [
            "id",
            "issue",
            "author",
            "description",
            "created_time",
        ]

    def validate(self, data, **kwargs):
        data["issue"] = self.context["issue"]
        data["author"] = self.context["author"]
        return data
