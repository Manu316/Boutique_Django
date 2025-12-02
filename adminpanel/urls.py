from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="admin_dashboard"),
    path("categorias/", views.admin_categorias, name="admin_categorias"),
    path("productos/", views.admin_productos, name="admin_productos"),
]