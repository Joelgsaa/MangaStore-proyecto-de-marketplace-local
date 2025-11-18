# Marketplace_local/MangaStore

Proyecto Django para venta de mangas.

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Joelgsaa/MangaStore-proyecto-de-marketplace-local.git
   cd marketplace_local 

2. Crear entorno virtual:
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate

3. - Instalar dependencias:
     pip install -r requirements.txt

4. Migrar base de datos:
   python manage.py migrate

5. Crear superusuario (opcional):
   python manage.py createsuperuser

6. Correr el servidor:
   python manage.py runserver
   Aparecera este link http://127.0.0.1:8000/

Funcionalidades
- Listado y detalle de productos
- Carrito de compras
- Checkout con Mercado Pago(no funciona)
- Panel de administración

iniciar sesion:
- Ingrsese en este link http://127.0.0.1:8000/login/
- pon tu nombre de usuario y contraseña de minimo 8 o 9 caracteres

CRUD o administracion:
- Ingrese a este link http://127.0.0.1:8000/admin/
-para que crees o modifiques productos

API:
- Ingrsese en este link http://127.0.0.1:8000/api/

Esta implementado codigos de mercado pago pero por varios errores externos esta no llega a concretar



