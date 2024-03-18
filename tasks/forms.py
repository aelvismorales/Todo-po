""" This module contains the forms for the tasks app."""

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task, TaskList


class CreateTaskListForm(forms.ModelForm):
    """Form for the TaskList model."""

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300  dark:focus:ring-torch-red-400"
            }
        ),
        error_messages={"required": _("The name of the task list is required.")},
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300 dark:focus:ring-torch-red-400"
            }
        ),
        error_messages={"required": _("The description of the task list is required.")},
    )

    class Meta:
        model = TaskList
        fields = ["name", "description"]

    # This definitions will be used in the template to render the form
    def clean(self):
        """Validate that name is capitalized."""
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        if name:
            cleaned_data["name"] = name.capitalize()
        if description:
            cleaned_data["description"] = description.capitalize()
        return cleaned_data

    def clean_name(self):
        """Validate that the name of the task list is not repeated."""
        name = self.cleaned_data["name"]
        if TaskList.objects.filter(name=name).exists():
            raise forms.ValidationError("The name of the task list already exists.")
        return name


class UpdateTaskListForm(forms.ModelForm):
    """Form for the TaskList model."""

    class Meta:
        model = TaskList
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(UpdateTaskListForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs[
            "class"
        ] = "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300  dark:focus:ring-torch-red-400"
        self.fields["description"].widget.attrs[
            "class"
        ] = "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300 dark:focus:ring-torch-red-400 "

    # This definitions will be used in the template to render the form
    def clean_name(self):
        """Validate that the name of the task list is unique among other task lists."""
        name = self.cleaned_data["name"]
        existing_task_lists = TaskList.objects.exclude(
            pk=self.instance.pk
        )  # Exclude current instance
        if existing_task_lists.filter(name=name).exists():
            raise forms.ValidationError("The name of the task list already exists.")
        return name

    def clean(self):
        """Capitalize name and description."""
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        if name:
            cleaned_data["name"] = name.capitalize()
        if description:
            cleaned_data["description"] = description.capitalize()
        return cleaned_data

    def save(self, commit=True):
        """Save the task list."""
        task_list = super(UpdateTaskListForm, self).save(commit=False)
        if commit:
            task_list.save()
        return task_list


class TaskForm(forms.ModelForm):
    """Form for the Task model."""

    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300  dark:focus:ring-torch-red-400"
            }
        ),
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300 dark:focus:ring-torch-red-400"
            }
        ),
    )
    completed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "w-6 h-6 text-torch-red-600 border-gray-300 rounded-md focus:ring-torch-red-300 dark:focus:ring-torch-red-400"
            }
        ),
        initial=False,
    )

    class Meta:
        model = Task
        fields = ["title", "description", "completed"]

    # Limpieza de los datos
    # Los datos que lleguen van a pasar por este proceso primero
    def clean(self):
        """Capitalize title and description."""
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")
        if title:
            cleaned_data["title"] = title.capitalize()
        if description:
            cleaned_data["description"] = description.capitalize()
        return cleaned_data


class UpdateTaskForm(forms.ModelForm):
    """Form for the Task model."""

    class Meta:
        model = Task
        fields = ["title", "description", "completed"]

    def __init__(self, *args, **kwargs):
        super(UpdateTaskForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs[
            "class"
        ] = "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300  dark:focus:ring-torch-red-400"
        self.fields["description"].widget.attrs[
            "class"
        ] = "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300 dark:focus:ring-torch-red-400"
        self.fields["completed"].widget.attrs[
            "class"
        ] = "w-6 h-6 text-torch-red-600 border-gray-300 rounded-md focus:ring-torch-red-300 dark:focus:ring-torch-red-400"

    # Limpieza de los datos
    # Los datos que lleguen van a pasar por este proceso primero
    def clean(self):
        """Capitalize title and description."""
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")
        if title:
            cleaned_data["title"] = title.capitalize()
        if description:
            cleaned_data["description"] = description.capitalize()
        return cleaned_data

    def save(self, commit=True):
        """Save the task."""
        task = super(UpdateTaskForm, self).save(commit=False)
        if commit:
            task.save()
        return task
