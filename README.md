# Lark Boutique – Sistema Web con Django

Lark Boutique es una aplicación web desarrollada con **Django 5** para la gestión de una boutique de ropa.  
Incluye dos interfaces principales:

- **Sitio público**: catálogo de productos, detalles, búsqueda, filtros y sección de looks.
- **Panel administrativo**: interfaz protegida para gestionar productos, categorías y looks.

---

## Características principales

### Sitio Público
- Listado de productos con búsqueda y filtros (talla, color).
- Detalle de producto con información completa.
- Lookbook con combinaciones de outfits.
- Vista de detalle de look mostrando prendas relacionadas.
- Página de contacto con envío real de correos.

### Panel Administrativo
- Login seguro con Django.
- CRUD de:
  - Categorías
  - Productos
  - Looks
- Eliminación segura con pantallas de confirmación.
- Configuración responsiva.

---

## Requisitos del sistema
- Python 3.10+
- Pip actualizado (python -m pip install --upgrade pip)
- Virtualenv recomendado
- Dependencias listadas en requirements.txt

## Instalación
- Clonar el repositorio
- Crear y activar el entorno virtual
    - python -m venv .venv
    - .venv\Scripts\activate
- pip install -r requirements.txt
- Realizar migraciones
    - python manage.py migrate --fake-initial
- Ejecutar servidor
    - python manage.py runserver