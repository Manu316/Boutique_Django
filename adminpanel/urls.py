from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "adminpanel"

urlpatterns = [
    # Login
    path('login/', auth_views.LoginView.as_view(
        template_name='adminpanel/login.html',
        redirect_authenticated_user=False
    ), name='login'),
    #Logout
    path("logout/", auth_views.LogoutView.as_view(next_page="adminpanel:login"), name="logout"),

    # Dashboard
    path('', views.admin_productos, name='dashboard'),

    # Categorías
    path('categorias/', views.admin_categorias, name='categorias'),
    path('categorias/nueva/', views.admin_categoria_nueva, name='categoria_nueva'),
    path('categorias/<int:idx>/editar/', views.admin_categoria_editar, name='categoria_editar'),
    path('categorias/<int:idx>/eliminar/', views.admin_categoria_eliminar, name='categoria_eliminar'),

    # Productos
    path('productos/', views.admin_productos, name='admin_productos'),
    path('productos/nuevo/', views.admin_producto_nuevo, name='producto_nuevo'),
    path('productos/<int:idx>/editar/', views.admin_producto_editar, name='producto_editar'),
    path('productos/<int:idx>/eliminar/', views.admin_producto_eliminar, name='producto_eliminar'),
]
