# Fundación Patrimonio Vivo

Siga estos pasos para instalar las dependencias, configurar la base de datos y ejecutar la aplicación.

## Requisitos

- Python 3.12 o superior.

## Instale las dependencias

Abra una terminal en la carpeta del proyecto e instale las dependencias indicadas en `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

Este archivo incluye Django, necesario para crear y ejecutar el proyecto.

## Cree un proyecto y una aplicación desde cero

Omita esta sección si va a utilizar este repositorio: ya contiene el proyecto `FundacionPatrimonioVivo` y la aplicación `core`. Ejecute estos comandos solo para iniciar un proyecto nuevo.

Para crear un proyecto Django en la carpeta actual, ejecute:

```powershell
python -m django startproject FundacionPatrimonioVivo .
```

Dentro de la carpeta del proyecto, cree una aplicación:

```powershell
python manage.py startapp core
```

Después, agregue `'core'` a `INSTALLED_APPS` en `FundacionPatrimonioVivo/settings.py`.

## Configure la base de datos y cree un administrador

El proyecto utiliza SQLite. Genere las migraciones de los modelos de `core` y aplíquelas para crear `db.sqlite3` si todavía no existe:

```powershell
python manage.py makemigrations core
python manage.py migrate
```

Si modifica los modelos más adelante, vuelva a ejecutar `makemigrations` y `migrate`.

Para crear un usuario administrador, ejecute:

```powershell
python manage.py createsuperuser
```

## Ejecute la aplicación

Inicie el servidor de desarrollo:

```powershell
python manage.py runserver
```

Abra <http://127.0.0.1:8000/home/> en el navegador para acceder a la aplicación. Para acceder al panel de administración, abra <http://127.0.0.1:8000/admin/> e inicie sesión con el usuario que creó.
