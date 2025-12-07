from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Producto, Categoria, Look, LookItem
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings  

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

    productos = look.productos.all()

    items = []
    for p in productos:
        items.append({
            "product_id": p.id,
            "product_name": p.nombre,
            "variant_sku": "",
            "note": "",
            "image": p.imagen,
        })

    return render(request, "catalog/look_detail.html", {
        "look": look,
        "items": items,
    })

def nosotros(request):
    return render(request, "catalog/nosotros.html")

def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        email = request.POST.get("email", "").strip()
        mensaje = request.POST.get("mensaje", "").strip()

        if not nombre or not email or not mensaje:
            messages.error(request, "Por favor, completa todos los campos.")
        else:
            cuerpo = (
                f"Nuevo mensaje desde el formulario de contacto:\n\n"
                f"Nombre: {nombre}\n"
                f"Email: {email}\n\n"
                f"Mensaje:\n{mensaje}"
            )

            try:
                destinatario = getattr(settings, "CONTACT_EMAIL", None) or settings.DEFAULT_FROM_EMAIL

                send_mail(
                    subject=f"Contacto Lark Boutique - {nombre}",
                    message=cuerpo,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[destinatario],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f"Ocurrió un error al enviar el correo: {e}")
            else:
                messages.success(request, "¡Gracias por escribirnos! Te responderemos pronto.")
                return redirect("contacto")

    return render(request, "contacto.html")