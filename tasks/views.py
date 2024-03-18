""" This file contains the views for the tasks app. """

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count

# from django.contrib import messages
from .forms import CreateTaskListForm, UpdateTaskForm, UpdateTaskListForm, TaskForm
from .models import TaskList, Task

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
        form = UpdateTaskListForm(
            request.POST, instance=task_list
        )  # Nos permite actualizar el objeto con los datos que vienen en el request por eso usamos el instance.
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
# * PASS
def add_task_to_task_list(request, task_list_id):  # Create a new task
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
                    "task": new_task.get_json(),
                }
            )
        return JsonResponse(
            {"status": "error", "message": "No se pudo agregar la tarea."}
        )
    return JsonResponse({"status": "error", "message": "No se pudo agregar la tarea."})


# TODO: Add login required decorator
# * PASS
def view_tasks(request, task_list_id):
    """View the tasks of a task list"""
    task_list = TaskList.objects.get(id=task_list_id)
    tasks = (
        task_list.task_set.all()
    )  # this will return all the tasks related to task_list.
    if is_ajax(request):
        tasks_data = [task.get_json() for task in tasks]
        return JsonResponse({"tasks": tasks_data})
    return render(
        request,
        "item_task/view_tasks.html",
        {
            "task_list": task_list,
            "tasks": tasks,
            "add_task_to_task_list_form": TaskForm(),
            "update_task_form": UpdateTaskForm(),
        },
    )


# TODO: Add login required decorator
# * PASS
def update_task(request, task_id):
    """Update a task"""
    if request.method == "POST":
        task = Task.objects.get(id=task_id)
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save(commit=False)
            updated_task.save()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Tarea actualizada con éxito.",
                    "task": updated_task.get_json(),
                }
            )
        return JsonResponse(
            {"status": "error", "message": "No se pudo actualizar la tarea."}
        )
    if request.method == "GET":
        task = Task.objects.get(id=task_id)
        return JsonResponse({"task": task.get_json()})
    return JsonResponse(
        {"status": "error", "message": "No se pudo actualizar la tarea."}
    )


# TODO : Add login required decorator
# * PASS
def delete_task(request, task_id):
    """Delete a task"""
    if request.method == "DELETE":
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Tarea eliminada con éxito.",
                }
            )
        except Task.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No se pudo eliminar la tarea, no existe.",
                }
            )
    return JsonResponse(
        {
            "status": "error",
            "message": "No se pudo eliminar la tarea, el metodo no es DELETE.",
        }
    )
