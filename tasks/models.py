"""Modelos de la aplicación tasks"""

from django.db import models
from django.template.defaultfilters import date as date_filter


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

    def get_json(self, success_message=None, exist_one=False):
        """Return the data of the task list in JSON format"""
        json_data = {
            "id": self.pk,
            "name": self.name,
            "description": self.description,
            "created": date_filter(self.created, "F d, Y") if self.created else "",
            "total_tasks": self.total_tasks(),
            "completed_tasks": self.completed_tasks(),
        }
        if success_message:
            json_data.update(
                {
                    "status": "success",
                    "message": success_message,
                    "exist_one": exist_one,
                }
            )
        return json_data


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
