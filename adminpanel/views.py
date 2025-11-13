from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto

CATEGORIES = [
    {"id": 1, "name": "Blusas",  "description": "Prendas superiores femeninas."},
    {"id": 2, "name": "Faldas",  "description": "Faldas casuales y formales."},
    {"id": 3, "name": "Interior","description": "Ropa interior y lencería."},
]

ADMIN_PRODUCTS = [
    {"id": 1, "name": "Blusa negra",      "category": "Blusas",  "stock": 15, "price": 450},
    {"id": 2, "name": "Falda roja",       "category": "Faldas",  "stock": 8,  "price": 399},
    {"id": 3, "name": "Calcetas verdes",  "category": "Interior","stock": 13, "price": 120},
]

def dashboard(request):
    return redirect('admin_categorias')

def admin_categorias(request):
    return render(request, "adminpanel/categorias.html", {
        "categories": CATEGORIES,
    })


def admin_productos(request):
    return render(request, "adminpanel/productos.html", {
        "products": ADMIN_PRODUCTS,
    })