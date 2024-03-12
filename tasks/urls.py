""" URL Configuration for tasks app."""

from django.urls import path

from . import views

urlpatterns = [
    path("task_list/", views.view_task_list, name="task_list"),
    path("create_task_list/", views.create_task_list, name="create_task_list"),
]
