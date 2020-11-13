from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .asana import create_task, create_project, update_task, update_project


class User(models.Model):
    gid = models.TextField(max_length=1024)
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.gid[:50]


class Project(models.Model):
    gid = models.TextField(max_length=1024, blank=True)
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.gid[:50]


class Task(models.Model):
    gid = models.TextField(max_length=1024, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField()

    def __str__(self):
        return self.gid[:50]


@receiver(pre_save, sender=Project)
def create_or_update_project(sender, instance, **kwargs):
    if not Project.objects.filter(pk=instance.pk).exists():
        instance.gid = create_project(project=instance)

    else:
        update_project(project=instance)


@receiver(pre_save, sender=Task)
def create_or_update_task(sender, instance, **kwargs):
    if not Task.objects.filter(pk=instance.pk).exists():
        instance.gid = create_task(task=instance)

    else:
        update_task(task=instance)
