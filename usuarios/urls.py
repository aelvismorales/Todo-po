"""todopo_django URL Configuration"""

from django.urls import path

from . import views

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("usuarios/", views.get_usuarios, name="usuarios"),
    path("login/", views.login_usuario, name="login"),
]
