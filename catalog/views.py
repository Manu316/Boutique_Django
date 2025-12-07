from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Producto, Categoria, Look, LookItem


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

    looks = Look.objects.filter(status="published")

    if tag:
        looks = [
            l for l in looks
            if tag in [t.lower() for t in l.tag_list()]
        ]

    return render(request, "catalog/look_list.html", {
        "looks": looks,
        "tag": tag,
    })

def look_detail(request, pk: int):
    look = get_object_or_404(Look, pk=pk)

    look_items = (
        LookItem.objects
        .filter(look=look)
        .select_related("product")
    )

    items = []
    for li in look_items:
        product = li.product
        items.append({
            "product_id": product.id,
            "product_name": product.nombre,
            "variant_sku": "",
            "note": li.note,
            "image": product.imagen,
        })

    return render(request, "catalog/look_detail.html", {
        "look": look,
        "items": items,
    })

def nosotros(request):
    return render(request, "catalog/nosotros.html")


def contacto(request):
    return render(request, "catalog/contacto.html")

