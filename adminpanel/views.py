from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms

# Datos simulados
CATEGORIES = [
    {"id": 1, "name": "Blusas",   "description": "Prendas superiores femeninas."},
    {"id": 2, "name": "Faldas",   "description": "Faldas casuales y formales."},
    {"id": 3, "name": "Interior", "description": "Ropa interior y lencería."},
]

ADMIN_PRODUCTS = [
    {"id": 1, "name": "Blusa negra",     "category": "Blusas",   "stock": 15, "price": 450},
    {"id": 2, "name": "Falda roja",      "category": "Faldas",   "stock": 8,  "price": 399},
    {"id": 3, "name": "Calcetas verdes", "category": "Interior", "stock": 13, "price": 120},
]


def _next_id(items):
    """Siguiente id incremental para las listas simuladas."""
    if not items:
        return 1
    return max(i["id"] for i in items) + 1


# Formularios
class CategoriaForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=50)
    description = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )


class ProductoForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=80)
    category = forms.ChoiceField(label="Categoría")
    stock = forms.IntegerField(label="Stock", min_value=0)
    price = forms.DecimalField(label="Precio", max_digits=8, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = [
            (c["name"], c["name"]) for c in CATEGORIES
        ]


# Dashboard
@login_required
def dashboard(request):
    return redirect('admin_productos')


# Categorías
@login_required
def admin_categorias(request):
    return render(request, "adminpanel/categorias.html", {
        "categories": CATEGORIES,
        "section": "categorias",
    })


@login_required
def admin_categoria_nueva(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            CATEGORIES.append({
                "id": _next_id(CATEGORIES),
                "name": form.cleaned_data["name"],
                "description": form.cleaned_data["description"],
            })
            return redirect("admin_categorias")
    else:
        form = CategoriaForm()

    return render(request, "adminpanel/categoria_form.html", {
        "form": form,
        "title": "Nueva categoría",
        "section": "categorias",
    })


@login_required
def admin_categoria_editar(request, pk: int):
    cat = next((c for c in CATEGORIES if c["id"] == pk), None)
    if not cat:
        return redirect("admin_categorias")

    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            cat["name"] = form.cleaned_data["name"]
            cat["description"] = form.cleaned_data["description"]
            return redirect("admin_categorias")
    else:
        form = CategoriaForm(initial={
            "name": cat["name"],
            "description": cat["description"],
        })

    return render(request, "adminpanel/categoria_form.html", {
        "form": form,
        "title": "Editar categoría",
        "section": "categorias",
    })


@login_required
def admin_categoria_eliminar(request, pk: int):
    global CATEGORIES
    CATEGORIES = [c for c in CATEGORIES if c["id"] != pk]
    return redirect("admin_categorias")


# Productos
@login_required
def admin_productos(request):
    return render(request, "adminpanel/productos.html", {
        "products": ADMIN_PRODUCTS,
        "section": "productos",
    })


@login_required
def admin_producto_nuevo(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ADMIN_PRODUCTS.append({
                "id": _next_id(ADMIN_PRODUCTS),
                "name": data["name"],
                "category": data["category"],
                "stock": int(data["stock"]),
                "price": float(data["price"]),
            })
            return redirect("admin_productos")
    else:
        form = ProductoForm()

    return render(request, "adminpanel/producto_form.html", {
        "form": form,
        "title": "Nuevo producto",
        "section": "productos",
    })


@login_required
def admin_producto_editar(request, pk: int):
    prod = next((p for p in ADMIN_PRODUCTS if p["id"] == pk), None)
    if not prod:
        return redirect("admin_productos")

    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            prod["name"] = data["name"]
            prod["category"] = data["category"]
            prod["stock"] = int(data["stock"])
            prod["price"] = float(data["price"])
            return redirect("admin_productos")
    else:
        form = ProductoForm(initial={
            "name": prod["name"],
            "category": prod["category"],
            "stock": prod["stock"],
            "price": prod["price"],
        })

    return render(request, "adminpanel/producto_form.html", {
        "form": form,
        "title": "Editar producto",
        "section": "productos",
    })


@login_required
def admin_producto_eliminar(request, pk: int):
    global ADMIN_PRODUCTS
    ADMIN_PRODUCTS = [p for p in ADMIN_PRODUCTS if p["id"] != pk]
    return redirect("admin_productos")


@login_required
def admin_logout(request):
    auth_logout(request)
    return redirect('adminpanel:login') 

