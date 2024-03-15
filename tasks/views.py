""" This file contains the views for the tasks app. """

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count

# from django.contrib import messages
from .forms import CreateTaskListForm, UpdateTaskListForm, TaskForm
from .models import TaskList

# Create your views here.


def is_ajax(request):
    """Return True if the request is an AJAX request."""
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


# CRUD
# TODO: Add login required decorator
def view_task_list(request):
    """View the task list"""
    task_list = TaskList.objects.all()

    if is_ajax(request):
        task_list_data = [task_list_item.get_json() for task_list_item in task_list]
        return JsonResponse({"task_lists": task_list_data})
    return render(
        request,
        "task_list/view_task_list.html",
        {
            "task_lists": task_list,
            "create_task_list_form": CreateTaskListForm(),
            "update_task_list_form": UpdateTaskListForm(),
            "add_task_to_task_list_form": TaskForm(),
        },
    )


# TODO: Add login required decorator
def create_task_list(request):  # This is only for the button to create a new task list
    """Create a new task list"""
    if request.method == "POST":
        form = CreateTaskListForm(request.POST)
        if form.is_valid():
            new_task_list = form.save()
            exist_one = False
            if TaskList.objects.aggregate(count=Count("id"))["count"] == 1:
                exist_one = True

            json_data = new_task_list.get_json(
                "Lista de tareas creada con éxito.", exist_one
            )
            return JsonResponse(json_data)
        return JsonResponse(
            {"status": "error", "message": "No se pudo crear la lista de tareas"}
        )
    return JsonResponse(
        {"status": "error", "message": "No se pudo crear la lista de tareas"}
    )


# TODO: Add login required decorator
def update_task_list(request, task_list_id):
    """Update a task list"""
    if request.method == "POST":
        task_list = TaskList.objects.get(id=task_list_id)
        form = UpdateTaskListForm(request.POST, instance=task_list)
        if form.is_valid():
            updated_task_list = form.save(commit=False)
            updated_task_list.save()
        return JsonResponse(
            {
                "status": "success",
                "message": "Lista de tareas actualizada con éxito.",
            }
        )

    return JsonResponse(
        {"status": "error", "message": "No se pudo actualizar la lista de tareas."}
    )


# TODO: Add login required decorator
def get_task_list(request, task_list_id):
    """Get a task list"""
    task_list = TaskList.objects.get(id=task_list_id)
    if task_list:
        return JsonResponse(
            {
                "id": task_list.pk,
                "name": task_list.name,
                "description": task_list.description,
            }
        )
    return JsonResponse(
        {"status": "error", "message": "No se pudo obtener la lista de tareas."}
    )


# TODO: Add login required decorator
def delete_task_list(request, task_list_id):
    """Delete a task list"""

    if request.method == "DELETE":
        try:
            last_one = False
            if TaskList.objects.aggregate(count=Count("id"))["count"] == 1:
                last_one = True
            task_list = TaskList.objects.get(id=task_list_id)
            task_list.delete()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Lista de tareas eliminada con éxito.",
                    "last_one": last_one,
                }
            )

        except TaskList.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No se pudo eliminar la lista de tareas, no existe.",
                }
            )

    return JsonResponse(
        {
            "status": "error",
            "message": "No se pudo eliminar la lista de tareas, el metodo no es DELETE.",
        }
    )


# TODO: Add login required decorator
def add_task_to_task_list(request, task_list_id):
    """Add a new task to a task list"""
    if request.method == "POST":
        task_list = TaskList.objects.get(id=task_list_id)
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.task_list = task_list
            new_task.save()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Tarea agregada con éxito.",
                }
            )
        return JsonResponse(
            {"status": "error", "message": "No se pudo agregar la tarea."}
        )
    return JsonResponse({"status": "error", "message": "No se pudo agregar la tarea."})
