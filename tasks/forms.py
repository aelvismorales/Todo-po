""" This module contains the forms for the tasks app."""

from django import forms
from .models import Task, TaskList


class CreateTaskListForm(forms.ModelForm):
    """Form for the TaskList model."""

    class Meta:
        model = TaskList
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(CreateTaskListForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs[
            "class"
        ] = "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300  dark:focus:ring-torch-red-400"
        self.fields["description"].widget.attrs[
            "class"
        ] = "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300 dark:focus:ring-torch-red-400 "

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


class TaskForm(forms.ModelForm):
    """Form for the Task model."""

    class Meta:
        model = Task
        fields = ["title", "description", "completed", "task_list"]
