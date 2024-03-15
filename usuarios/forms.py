"""Formularios para la aplicación de usuarios."""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class CustomUserCreationForm(UserCreationForm):
    """Formulario de creación de usuario personalizado."""

    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300  dark:focus:ring-torch-red-400",
            }
        ),
        required=True,
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300  dark:focus:ring-torch-red-400"
            }
        ),
        required=True,
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-2 focus:outline-none focus:ring-torch-red-300  dark:focus:ring-torch-red-400"
            }
        ),
        required=True,
        # help_text="Ingrese la misma contraseña que antes, para verificación.",
    )

    def clean_username(self):
        """Validar que el nombre de usuario no exista."""
        username = self.cleaned_data["username"].lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya existe.")
        return username

    def clean_password2(self):
        """Validar que las contraseñas coincidan."""
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        """Guardar el usuario."""
        if commit:
            user = User.objects.create_user(
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password1"],
            )
            return user
        # Me permite guarda rla instancia del usuario sin aun guardarlo en la base de datos, para despues realizar el user.save()
        return super().save(commit=commit)


class LoginUserForm(forms.Form):
    """Formulario de inicio de sesión."""

    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring focus:border-torch-red-200 focus:ring-torch-red-200 focus:ring-opacity-50 dark:focus:ring-torch-red-400 dark:focus:ring-opacity-70",
            }
        ),
        required=True,
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring focus:border-torch-red-200 focus:ring-torch-red-200 focus:ring-opacity-50 dark:focus:ring-torch-red-400 dark:focus:ring-opacity-70"
            }
        ),
        required=True,
    )

    def user_authenticate(self):
        """Autenticar al usuario."""
        if self.is_valid():
            user = authenticate(
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password"],
            )
            if user is not None:
                return user
            raise forms.ValidationError("Usuario o contraseña incorrectos.")
        raise forms.ValidationError("Usuario o contraseña incorrectos.")


# Path: todopo_django/usuarios/forms.py
# Compare this snippet from todopo_django/usuarios/urls.py:
# """todopo_django URL Configuration"""
