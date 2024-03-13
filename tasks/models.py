"""Modelos de la aplicación tasks"""

from django.db import models


# Create your models here.
class TaskList(models.Model):
    """Modelo de la lista de tareas"""

    name = models.CharField(
        max_length=100
    )  # This will be the kind of list setting for the user
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def total_tasks(self):
        """Return the total of tasks in the list"""
        total = self.task_set.count() if self.task_set.count() else 0
        return total

    def completed_tasks(self):
        """Return the total of completed tasks in the list"""
        total = (
            self.task_set.filter(completed=True).count()
            if self.task_set.filter(completed=True).count()
            else 0
        )
        return total


class Task(models.Model):
    """Modelo de la tarea"""

    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    task_list = models.ForeignKey(
        TaskList, on_delete=models.CASCADE
    )  # If the task list is deleted all the tasks that contain it will be deleted too

    def __str__(self):
        return str(self.title)
