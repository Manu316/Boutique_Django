from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Producto, Categoria, Look


def home(request):
    return redirect("product_list")

def product_list(request):
    q = request.GET.get("q", "").strip()
    size = request.GET.get("size", "").strip()
    color = request.GET.get("color", "").strip()

    products = Producto.objects.select_related("categoria").all()

    if q:
        products = products.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(categoria__nombre__icontains=q)
        )

    if size:
        products = products.filter(talla=size)

    if color:
        products = products.filter(color__icontains=color)

    sizes = [code for code, _ in Producto.TALLAS]
    colors = (
        Producto.objects.exclude(color="")
        .values_list("color", flat=True)
        .distinct()
        .order_by("color")
    )

    return render(request, "catalog/product_list.html", {
        "products": products,
        "q": q,
        "size": size,
        "color": color,
        "sizes": sizes,
        "colors": colors,
    })


def product_detail(request, pk: int):
    product = get_object_or_404(Producto, pk=pk)
    return render(request, "catalog/product_detail.html", {
        "product": product
    })

def look_list(request):
    tag = request.GET.get("tag", "").strip().lower()

    looks = Look.objects.filter(status="published").order_by("-created_at")

    if tag:
        looks = looks.filter(tags__icontains=tag)

    return render(request, "catalog/look_list.html", {
        "looks": looks,
        "tag": tag,
    })

def look_detail(request, pk: int):
    look = get_object_or_404(Look, pk=pk, status="published")

    return render(request, "catalog/look_detail.html", {
        "look": look,
    })

def nosotros(request):
    return render(request, "catalog/nosotros.html")


def contacto(request):
    return render(request, "catalog/contacto.html")
