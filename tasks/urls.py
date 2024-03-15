""" URL Configuration for tasks app."""

from django.urls import path

from . import views

urlpatterns = [
    path("task_list/", views.view_task_list, name="task_list"),
    path("create_task_list/", views.create_task_list, name="create_task_list"),
    path(
        "update_task_list/<int:task_list_id>/",
        views.update_task_list,
        name="update_task_list",
    ),
    path(
        "delete_task_list/<int:task_list_id>/",
        views.delete_task_list,
        name="delete_task_list",
    ),
    path(
        "get_task_list/<int:task_list_id>/",
        views.get_task_list,
        name="get_task_list",
    ),
    path(
        "add_task_to_task_list/<int:task_list_id>/",
        views.add_task_to_task_list,
        name="add_task_to_task_list",
    ),
]
