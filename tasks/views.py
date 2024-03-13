""" This file contains the views for the tasks app. """

from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CreateTaskListForm, UpdateTaskListForm
from .models import TaskList

# Create your views here.


# CRUD
# TODO: Add login required decorator
def view_task_list(request):
    """View the task list"""
    task_list = TaskList.objects.all()
    return render(
        request,
        "task_list/view_task_list.html",
        {
            "task_lists": task_list,
            "create_task_list_form": CreateTaskListForm(),
            "update_task_list_form": UpdateTaskListForm(),
        },
    )


# TODO: Add login required decorator
def create_task_list(request):  # This is only for the button to create a new task list
    """Create a new task list"""
    if request.method == "POST":
        form = CreateTaskListForm(request.POST)
        print("llegue a crear la lista de tareas")
        if form.is_valid():
            form.save()
            messages.success(request, "Lista de tareas creada con éxito.")
            return redirect("task_list")
        return render(request, "task_list/view_task_list.html", {"form": form})
    return redirect("task_list")


# TODO: Add login required decorator
def update_task_list(request, task_list_id):
    """Update a task list"""
    if request.method == "POST":
        task_list = TaskList.objects.get(id=task_list_id)
        task_list.name = request.POST["name"]
        task_list.description = request.POST["description"]
        task_list.save()
        messages.success(request, "Lista de tareas actualizada con éxito.")
        return redirect("task_list")
    return redirect("task_list")


# TODO: Add login required decorator
def delete_task_list(request, task_list_id):
    """Delete a task list"""
    task_list = TaskList.objects.get(id=task_list_id)
    task_list.delete()
    messages.success(request, "Lista de tareas eliminada con éxito.")
    return redirect("task_list")
