from django.shortcuts import render
from .models import Projects, Issues, Comments
from .serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


# Create your views here.


class ViewSetProjects(ModelViewSet):
    """Acces API Control Projects"""

    permission_required = "QC.view_micontrolthickness"
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Projects.objects.filter(Q(author=self.request.user) | Q(contributor=self.request.user))
        product = self.request.GET.get("product")
        # filter on product
        if product is not None:
            queryset = queryset.filter(product=product)

        return queryset
