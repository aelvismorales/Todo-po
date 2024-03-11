"""Formularios para la aplicación de usuarios."""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """Formulario de creación de usuario personalizado."""

    username = forms.CharField(label="Nombre de usuario", max_length=150)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
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
        else:
            # Me permite guarda rla instancia del usuario sin aun guardarlo en la base de datos, para despues realizar el user.save()
            return super().save(commit=commit)


# Path: todopo_django/usuarios/forms.py
# Compare this snippet from todopo_django/usuarios/urls.py:
# """todopo_django URL Configuration"""
