from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from catalog.models import Categoria, Producto, Look

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]
        labels = {
            "nombre": "Nombre",
            "descripcion": "Descripción",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej. Blusas",
            }),
            "descripcion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Descripción breve",
            }),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "categoria", "descripcion", "talla",
                  "color", "stock", "precio", "imagen"]
        labels = {
            "nombre": "Nombre",
            "categoria": "Categoría",
            "descripcion": "Descripción",
            "talla": "Talla",
            "color": "Color",
            "stock": "Stock",
            "precio": "Precio",
            "imagen": "Imagen del producto",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not Categoria.objects.exists():
            self.fields["categoria"].required = False
            self.fields["categoria"].queryset = Categoria.objects.none()
            self.fields["categoria"].widget = forms.Select(
            choices=[("", "Sin categoría")]
            )
        else:
            self.fields["categoria"].widget.attrs.update({"class": "form-select"})

        for name, field in self.fields.items():
            if name == "categoria":
                continue
            css = "form-control"
            if name == "imagen":
                css = "form-control"
            field.widget.attrs.setdefault("class", css)

class LookForm(forms.ModelForm):
    class Meta:
        model = Look
        fields = ["name", "status", "notes", "tags", "cover", "productos"]
        labels = {
            "name": "Nombre del look",
            "status": "Estado",
            "notes": "Notas",
            "tags": "Tags (separados por comas)",
            "cover": "Imagen de portada",
                      "productos": "Productos que componen el look",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "tags": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "boho, verano, casual",
                }
            ),
            "cover": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "productos": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["productos"].queryset = Producto.objects.order_by("nombre")

@login_required
def dashboard(request):
    return redirect("adminpanel:admin_productos")


@login_required
def admin_categorias(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("adminpanel:categorias")
    else:
        form = CategoriaForm()

    categorias = Categoria.objects.all().order_by("nombre")

    return render(request, "adminpanel/categorias.html", {
        "categories": categorias,
        "form": form,
        "section": "categorias",
    })

@login_required
def admin_categoria_nueva(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("adminpanel:categorias")
    else:
        form = CategoriaForm()

    return render(request, "adminpanel/categoria_form.html", {
        "form": form,
        "title": "Nueva categoría",
        "section": "categorias",
    })

@login_required
def admin_categoria_editar(request, pk: int):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("adminpanel:categorias")
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, "adminpanel/categoria_form.html", {
        "form": form,
        "title": "Editar categoría",
        "section": "categorias",
    })

@login_required
def admin_categoria_eliminar(request, pk: int):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == "POST":
        categoria.delete()
        return redirect("adminpanel:categorias")

    return render(request, "adminpanel/confirm_delete.html", {
        "obj": categoria,
        "cancel_url": "adminpanel:categorias",
        "section": "categorias",
    })

@login_required
def admin_productos(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("adminpanel:admin_productos")
    else:
        form = ProductoForm()

    productos = Producto.objects.select_related("categoria").all().order_by("nombre")

    return render(request, "adminpanel/productos.html", {
        "products": productos,
        "form": form,
        "section": "productos",
    })

@login_required
def admin_producto_nuevo(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("adminpanel:admin_productos")
    else:
        form = ProductoForm()

    return render(request, "adminpanel/producto_form.html", {
        "form": form,
        "title": "Nuevo producto",
        "section": "productos",
    })


@login_required
def admin_producto_editar(request, pk: int):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("adminpanel:admin_productos")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "adminpanel/producto_form.html", {
        "form": form,
        "title": "Editar producto",
        "section": "productos",
    })


@login_required
def admin_producto_eliminar(request, pk: int):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        producto.delete()
        return redirect("adminpanel:admin_productos")


    return render(request, "adminpanel/confirm_delete.html", {
        "obj": producto,
        "cancel_url": "adminpanel:admin_productos",
        "section": "productos",
    })

@login_required
def admin_looks(request):
    looks = Look.objects.all().order_by("-id")
    return render(request, "adminpanel/looks.html", {
        "looks": looks,
        "section": "looks",
    })

@login_required
def admin_look_nuevo(request):
    if request.method == "POST":
        form = LookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("adminpanel:looks")
    else:
         form = LookForm()

    return render(request, "adminpanel/look_form.html", {
        "form": form,
        "title": "Nuevo look",
        "section": "looks",
    })


@login_required
def admin_look_editar(request, pk: int):
    look = get_object_or_404(Look, pk=pk)

    if request.method == "POST":
        form = LookForm(request.POST, request.FILES, instance=look)
        if form.is_valid():
            form.save()
            return redirect("adminpanel:looks")
    else:
        form = LookForm(instance=look)

    return render(request, "adminpanel/look_form.html", {
        "form": form,
        "title": "Editar look",
        "section": "looks",
    })

@login_required
def admin_look_eliminar(request, pk: int):
    look = get_object_or_404(Look, pk=pk)

    if request.method == "POST":
        look.delete()
        return redirect("adminpanel:looks")

    return render(request, "adminpanel/confirm_delete.html", {
        "obj": look,
        "cancel_url": "adminpanel:looks",
        "section": "looks",
    })