from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Projects(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titre")
    description = models.CharField(max_length=2000, verbose_name="Description")
    type = models.CharField(max_length=255, verbose_name="Type")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Auteur")
    contributor = models.ManyToManyField(User, related_name="project_contributor", verbose_name="Contributeur")

    def __str__(self):
        return self.title


class Issues(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True, verbose_name="Projet")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Auteur")
    contributor = models.ManyToManyField(User, related_name="issue_contributor", verbose_name="Contributeur")
    title = models.CharField(max_length=255, verbose_name="Titre")
    description = models.CharField(max_length=2000, verbose_name="Description")
    tag = models.CharField(max_length=50, verbose_name="Tag")
    priority = models.CharField(max_length=50, verbose_name="Priorité")
    status = models.CharField(max_length=50, verbose_name="status")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return self.title


class Comments(models.Model):
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE, null=True, verbose_name="Probleme")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Auteur")
    description = models.CharField(max_length=2000, verbose_name="Description")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
