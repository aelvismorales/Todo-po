""" This file contains the views for the tasks app. """

from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CreateTaskListForm
from .models import TaskList

# Create your views here.


# CRUD
def view_task_list(request):
    """View the task list"""
    task_list = TaskList.objects.all()
    return render(
        request,
        "task_list/view_task_list.html",
        {"task_list": task_list, "create_task_list_form": CreateTaskListForm()},
    )


def create_task_list(request):  # This is only for the button to create a new task list
    """Create a new task list"""
    if request.method == "POST":
        form = CreateTaskListForm(request.POST)
        print("llegue a crear la lista de tareas")
        if form.is_valid():
            form.save()
            messages.success(request, "Lista de tareas creada con éxito.")
            return redirect("task_list")
        return render(request, "task_list/create_task_list.html", {"form": form})
