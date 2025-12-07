from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=60)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TALLAS = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("UNI", "Única"),
    ]

    nombre = models.CharField(max_length=80)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        related_name="productos",
        null=True,
        blank=True,
    )
    descripcion = models.TextField(blank=True)
    talla = models.CharField(max_length=5, choices=TALLAS, blank=True)
    color = models.CharField(max_length=30, blank=True)
    stock = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

class Look(models.Model):
    STATUS_CHOICES = [
        ("draft", "Borrador"),
        ("published", "Publicado"),
    ]

    name = models.CharField("Nombre", max_length=100)
    status = models.CharField("Estado", max_length=10, choices=STATUS_CHOICES, default="draft")
    notes = models.TextField("Notas", blank=True)
    tags = models.CharField(
        "Tags",
        max_length=200,
        blank=True,
        help_text="Escribe etiquetas separadas por comas. Ej: boho, verano",
    )
    cover = models.ImageField(
        "Portada",
        upload_to="looks/",
        blank=True,
        null=True,
    )
    productos = models.ManyToManyField(Producto, related_name="looks", blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]

class LookItem(models.Model):
    look = models.ForeignKey(
        Look,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="look_items",
    )
    note = models.CharField("Nota", max_length=200, blank=True)

    class Meta:
        verbose_name = "Prenda del look"
        verbose_name_plural = "Prendas del look"

    def __str__(self):
        return f"{self.product} en {self.look}"