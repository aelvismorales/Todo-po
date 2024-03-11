"""Views for the usuarios app."""

from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm


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
            form.save()  # Save the user to the database, this will create automate the user
            # Redireccionar a la pagina de usuarios
            return redirect("usuarios")
        return render(request, "registro.html", {"registro_form": form})
    return render(request, "registro.html", {"registro_form": CustomUserCreationForm()})


def get_usuarios(request):
    """Render la pagina de usuarios"""
    if request.method == "GET":
        usuarios = User.objects.all()
        print(usuarios)
        return render(request, "usuarios.html", {"usuarios": usuarios})
