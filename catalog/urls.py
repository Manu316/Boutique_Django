from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Catálogo
    path("productos/", views.product_list, name="product_list"),
    path("productos/<int:pk>/", views.product_detail, name="product_detail"),

    # Lookbook
    path("looks/", views.look_list, name="look_list"),
    path("looks/<int:pk>/", views.look_detail, name="look_detail"),   

    # Admin Panel
    path('adminpanel/', include('adminpanel.urls')),
 
]
