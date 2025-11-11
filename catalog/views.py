from django.shortcuts import render, redirect

# ==== PLACEHOLDERS ====
PRODUCTS = [
    {
        "id": 1,
        "name": "Vestido Ceñido Celeste",
        "category": "Vestidos",
        "description": "Vestido ceñido en tono celeste, ideal para primavera.",
        "tags": ["celeste", "primavera", "casual", "vestido"],
        "variants": [
            {
                "sku": "VCC-M-CEL",
                "size": "M", "color": "Celeste",
                "images": ["img/productos/vestido_cenido_celeste.jpg"]
            },
        ],
    },
    {
        "id": 2,
        "name": "Vestido Ceñido Rojo",
        "category": "Vestidos",
        "description": "Corte ceñido para eventos elegantes.",
        "tags": ["noche", "elegante", "vestido", "rojo"],
        "variants": [
            {
                "sku": "VCR-M-ROJ",
                "size": "M", "color": "Rojo",
                "images": ["img/productos/vestido_cenido_rojo.jpg"]
            }
        ],
    },
    {
        "id": 3,
        "name": "Vestido Largo Negro",
        "category": "Vestidos",
        "description": "Clásico y sofisticado.",
        "tags": ["clasico", "negro", "vestido", "elegante"],
        "variants": [
            {
                "sku": "VL-L-NEG",
                "size": "L", "color": "Negro",
                "images": ["img/productos/vestido_largo.jpg"]
            }
        ],
    },
    {
        "id": 4,
        "name": "Vestido Print Floral",
        "category": "Vestidos",
        "description": "Estampado floral vibrante.",
        "tags": ["primavera", "casual", "vestido", "floral"],
        "variants": [
            {
                "sku": "VPF-S-FLO",
                "size": "S", "color": "Floral",
                "images": ["img/productos/vestido_print.jpg"]
            }
        ],
    },    
]

LOOKS = [
    {
        "id": 1,
        "name": "Look Boho Verano",
        "status": "published",
        "notes": "Perfecto para día caluroso.",
        "tags": ["boho", "verano"],
        "cover": "https://placehold.co/900x900?text=Look+Boho",
        "items": [
            {"product_id": 1, "variant": "BL-LIN-M-VER", "note": "Remangar mangas"},
            {"product_id": 2, "variant": "PT-PLZ-M-NEG"},
        ],
    },
    {
        "id": 2,
        "name": "Look Casual Floral",
        "status": "published",
        "notes": "",
        "tags": ["casual"],
        "cover": "https://placehold.co/900x900?text=Look+Floral", 
        "items": [
            {"product_id": 3, "variant": "VS-FLR-L-MLT"},
        ],
    },
]

def home(request):
    return redirect("product_list")

# ----- Productos -----
def product_list(request):
    q = request.GET.get("q", "").strip().lower()
    size = request.GET.get("size", "").strip().upper()
    color = request.GET.get("color", "").strip()

    products = PRODUCTS
    if q:
        products = [
            p for p in products
            if q in p["name"].lower()
            or q in p["description"].lower()
            or any(q in v["sku"].lower() for v in p["variants"])
        ]
    if size:
        products = [
            p for p in products
            if any(v["size"].upper() == size for v in p["variants"])
        ]
    if color:
        products = [
            p for p in products
            if any(color.lower() in v["color"].lower() for v in p["variants"])
        ]

    sizes = ["XS","S","M","L","XL","UNI"]
    colors = sorted({v["color"] for p in PRODUCTS for v in p["variants"]})

    return render(request, "catalog/product_list.html", {
        "products": products,
        "q": q, "size": size, "color": color,
        "sizes": sizes, "colors": colors,
    })

def product_detail(request, pk: int):
    product = next((p for p in PRODUCTS if p["id"] == pk), None)
    if not product:
        return render(request, "404.html", status=404)
    cover = None
    for v in product["variants"]:
        if v["images"]:
            cover = v["images"][0]
            break
    # agrupar por color
    by_color = {}
    for v in product["variants"]:
        by_color.setdefault(v["color"], []).append(v)

    # Mostrar galería solo si hay más de una variante o más de una imagen en alguna variante
    has_gallery = (len(product["variants"]) > 1) or any(
        len(v.get("images", [])) > 1 for v in product["variants"]
    )        

    return render(request, "catalog/product_detail.html", {
        "product": product,
        "cover": cover,
        "by_color": by_color,
        "has_gallery": has_gallery,
    })

# ----- Looks -----
def look_list(request):
    tag = request.GET.get("tag", "").strip().lower()
    looks = [l for l in LOOKS if l["status"] == "published"]
    if tag:
        looks = [l for l in looks if tag in [t.lower() for t in l["tags"]]]
    return render(request, "catalog/look_list.html", {"looks": looks, "tag": tag})

def look_detail(request, pk: int):
    look = next((l for l in LOOKS if l["id"] == pk), None)
    if not look:
        return render(request, "404.html", status=404)

    # imagen de portada
    if not look.get["cover"]:
        first_img = None
        for it in look["items"]:
            prod = next((p for p in PRODUCTS if p["id"] == it["product_id"]), None)
            if not prod:
                continue
            for v in prod["variants"]:
                if v["images"]:
                    first_img = v["images"][0]
                    break
            if first_img:
                look["cover"] = first_img
                break

    rich_items = []
    for it in look["items"]:
        prod = next((p for p in PRODUCTS if p["id"] == it["product_id"]), None)
        if not prod:
            continue
        img = None
        for v in prod["variants"]:
            if v["sku"] == it["variant"] and v["images"]:
                img = v["images"][0]
                break
        rich_items.append({
            "product_id": prod["id"],
            "product_name": prod["name"],
            "variant_sku": it["variant"],
            "note": it.get("note", ""),
            "image": img,
        })

    return render(request, "catalog/look_detail.html", {"look": look, "items": rich_items})