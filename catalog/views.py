from django.shortcuts import render, redirect

# ==== PLACEHOLDERS ====
PRODUCTS = [
    {
        "id": 1,
        "name": "Blusa Lino",
        "brand": "Local",
        "category": "Blusas",
        "description": "Blusa fresca de lino para verano.",
        "tags": ["boho", "verano"],
        "variants": [
            {
                "sku": "BL-LIN-S-VER",
                "size": "S", "color": "Verde",
                "images": ["https://placehold.co/600x600?text=Blusa+Verde+S"]
            },
            {
                "sku": "BL-LIN-M-VER",
                "size": "M", "color": "Verde",
                "images": ["https://placehold.co/600x600?text=Blusa+Verde+M"]
            },
        ],
    },
    {
        "id": 2,
        "name": "Pantalón Palazzo",
        "brand": "Trendy",
        "category": "Pantalones",
        "description": "Palazzo cómodo, tiro alto.",
        "tags": ["casual"],
        "variants": [
            {
                "sku": "PT-PLZ-M-NEG",
                "size": "M", "color": "Negro",
                "images": ["https://placehold.co/600x600?text=Palazzo+Negro"]
            }
        ],
    },
    {
        "id": 3,
        "name": "Vestido Floral",
        "brand": "Local",
        "category": "Vestidos",
        "description": "Corte A, estampado floral.",
        "tags": ["primavera", "casual"],
        "variants": [
            {
                "sku": "VS-FLR-L-MLT",
                "size": "L", "color": "Multicolor",
                "images": ["https://placehold.co/600x600?text=Vestido+Floral"]
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

    return render(request, "catalog/product_detail.html", {
        "product": product,
        "cover": cover,
        "by_color": by_color,
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
    if not look["cover"]:
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
            "brand": prod["brand"],
            "variant_sku": it["variant"],
            "note": it.get("note", ""),
            "image": img,
        })

    return render(request, "catalog/look_detail.html", {"look": look, "items": rich_items})