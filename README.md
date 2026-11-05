# Fundación Patrimonio Vivo

Aplicación Django para consultar un catálogo de lugares patrimoniales y, con los permisos correspondientes, agregar y editar registros.

## Requisitos

- Python 3.12 o superior.
- PowerShell en Windows (o una terminal equivalente).

Si usa CMD en Windows, consulte [CONFIGURACION_WINDOWS.txt](./CONFIGURACION_WINDOWS.txt)
para configurar la clave secreta y preparar la base de datos paso a paso.

## Instalación

Clone o descargue este repositorio y abra la terminal en su carpeta raíz. Cree y active un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale las dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Configuración y base de datos

La aplicación requiere una clave secreta en la variable de entorno `DJANGO_SECRET_KEY`. Genere una clave local aleatoria y habilite el modo de desarrollo en la terminal actual:

```powershell
$env:DJANGO_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(50))"
$env:DJANGO_DEBUG = "True"
```

Estas variables solo permanecen disponibles en esa terminal. Genere una nueva clave para su propio entorno; no la escriba en el código, en este archivo ni en Git. Para producción, mantenga `DJANGO_DEBUG` desactivado y configure `DJANGO_ALLOWED_HOSTS` con los dominios autorizados.

La base de datos SQLite (`db.sqlite3`) se crea localmente y no se distribuye. Aplique las migraciones y cargue los datos de demostración:

```powershell
python manage.py migrate
python manage.py loaddata demo_data
```

El fixture `core/fixtures/demo_data.json` agrega seis categorías y siete lugares patrimoniales. Cárguelo una vez en una base vacía.

## Usuarios y permisos de prueba

Cree un administrador para acceder al panel de Django:

```powershell
python manage.py createsuperuser
```

Inicie el servidor y abra <http://127.0.0.1:8000/admin/>. Desde el panel:

1. En **Autenticación y autorización > Grupos**, cree un grupo, por ejemplo, `Gestores de lugares`.
2. Asígnele los permisos **Can add lugar patrimoniales** y **Can change lugar patrimoniales**.
3. En **Usuarios**, cree un usuario de prueba, déjelo activo y agréguelo al grupo. No es necesario marcarlo como administrador ni como miembro del staff para usar las pantallas de la aplicación.

El usuario del grupo podrá iniciar sesión en la aplicación, agregar lugares y editar los existentes. Para probar el acceso de solo lectura, use un usuario activo sin esos permisos: el catálogo seguirá disponible, pero las operaciones de edición estarán restringidas. Las contraseñas de los usuarios de prueba se establecen localmente y nunca deben agregarse al repositorio.

## Ejecutar

Con las variables de entorno configuradas en la terminal actual:

```powershell
python manage.py runserver
```

Abra <http://127.0.0.1:8000/> para usar la aplicación. El catálogo está en <http://127.0.0.1:8000/catalogo/> y el panel administrativo en <http://127.0.0.1:8000/admin/>.

## Seguridad

- No incluya claves, contraseñas, archivos `.env` ni bases de datos locales en Git.
- Si una clave secreta ya se publicó, considérela comprometida: genere otra y, si necesita eliminarla también del historial público, coordine la reescritura del historial con quienes hayan clonado el repositorio.
- El servidor incluido es para desarrollo; antes de publicar la aplicación, revise la lista de despliegue de seguridad de Django y configure HTTPS, `DJANGO_ALLOWED_HOSTS` y los ajustes de producción.
