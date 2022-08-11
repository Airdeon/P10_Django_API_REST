from rest_framework import serializers
from .models import Projects, Issues, Comments
from Accounts.serializers import ProjectUserSerializer


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
