"""Views for the usuarios app."""

from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginUserForm


# Create your views here.
def registro(request):
    """Render la pagina de registro"""
    if request.method == "GET":
        return render(
            request, "registro.html", {"registro_form": CustomUserCreationForm()}
        )

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = (
                form.save()
            )  # Save the user to the database, this will create automate the user
            # Redireccionar a la pagina de usuarios
            login(request, user)
            messages.success(request, "Usuario registrado con éxito.")
            return redirect("usuarios")
        return render(request, "registro.html", {"registro_form": form})
    return render(request, "registro.html", {"registro_form": CustomUserCreationForm()})


def login_usuario(request):
    """Render la pagina de login"""
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("task_list")
        return render(request, "login.html", {"login_form": LoginUserForm()})
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            # Redireccionar a la pagina de usuarios
            user = User.objects.get(username=form.cleaned_data["username"])
            if user.check_password(form.cleaned_data["password"]):
                login(request, user)
                messages.success(request, "Usuario logueado con éxito.")
                return redirect("task_list")
            return render(
                request,
                "login.html",
                {"login_form": form},
                {"error": "Usuario o contraseña incorrectos."},
            )
        return render(request, "login.html", {"login_form": form})
    return render(request, "login.html", {"login_form": LoginUserForm()})


@login_required
def logout_usuario(request):
    """Render la pagina de logout"""
    if request.user.is_authenticated:
        logout(request)
        return redirect("login")


@login_required
def get_usuarios(request):
    """Render la pagina de usuarios"""
    if request.method == "GET":
        usuarios = User.objects.all()
        # print(usuarios)
        return render(request, "usuarios.html", {"usuarios": usuarios})
    return render(request, "usuarios.html", {"usuarios": User.objects.all()})
