# Plantilla básica de un proyecto de Django con Django Rest Framework

El objetivo de este repositorio es usarlo como una plantilla, esqueleto o también llamado `boilerplate` inicial para cualquier proyecto de API REST que use Django.

La finalidad es que sirva de guía y permita al desarrollador enfocarse en escribir código y no en invertir demasiado tiempo en la inicialización y configuración del proyecto.

## Live mode

https://hackademy-drf-boilerplate.herokuapp.com/

### Test user credentials

username: testuser
password: testuser

## Tecnologías incluidas:
- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
- [Python decouple](https://pypi.org/project/python-decouple/)
- [Django-cors-headers](https://pypi.org/project/django-cors-headers/)
- [Dj-database-url](https://pypi.org/project/dj-database-url/)
- [WhiteNoise y Brotli](https://pypi.org/project/whitenoise/)
- [Gunicorn](https://pypi.org/project/gunicorn/)
- [django-heroku](https://pypi.org/project/django-heroku/)

### Para el ambiente de desarrollo usando pipfile se incluye también:
- [flake8](https://pypi.org/project/flake8/) para el linting
- [black](https://pypi.org/project/black/) para formatear el código
- [isort](https://pypi.org/project/isort/) para formatear y ordenar los imports

Opcional. Recomendaciones nivel intermedio - avanzado:
- [Pre-commit](https://pre-commit.com/) para chequear y arreglar nuestro código con las convenciones de los commits antes de publicar el código a un repositorio remoto


## Existen varias maneras de levantar el proyecto
1. [pipenv](#)
2. [venv](#)

En todos los casos antes de levantarlo se deben cumplir los siguientes requisitos:

- Crear un archivo de configuración `.env` con las variables de entorno necesarias a partir del archivo `.env-example`.

        $ cp .env-example .env

- Tener instalado o levantado una base de datos ya sea local o en la nube. Los datos de conexión tienen que ser incluidos en el archivo `.env` donde corresponda.

- Concluido el proceso de desplieque, se debe levantar el servidor y si es la primera vez se debe ejecutar el comando `python manage.py migrate` para sincronizar la base de datos. Después ese comando se usará a demanda cuando se creen nuevos modelos (leer la documentación).

- Opcional para el ambiente de desarrollo:

    - Usar WhiteNoise para el manejo de archivos estáticos

            $ python manage.py runserver --nostatic

## Cómo levantar el proyecto usando pipenv (1):

- Instalar pipenv

        $ pip install pipenv

- Instalar la versión de python indicada

        $ pipenv install --python 3.8.12

    - Opcional: instalar las dependencias regulares sumando las de desarrollo también

            $ pipenv install --python 3.8.12 --dev

- Activar el entorno virtual

        $ pipenv shell

- Levantar el servidor

        $ cd api

        $ python manage.py runserver

- Para desactivar el entorno virtual

        $ exit

#### Cuidado!
> **Al cambiar la carpeta del proyecto a otra ruta se rompe la referencia entre el entorno virtual creado con pipenv y el proyecto en sí, causando como consecuencia que no se pueda usar más nunca.**
> **Para evitar eso, se puede crear el entorno virtual dentro de la carpeta del proyecto (antes de hacer `$ pipenv install`) creando la siguiente variable de entorno**

        $ export PIPENV_VENV_IN_PROJECT=1


### Comandos útiles de pipenv

- Instalar una nueva dependencia

        $ pipenv install <dependencia>

    - Opcional: instalar una dependencia de desarrollo

            $ pipenv install <dependencia> --dev

- Actualizar las dependencias

        $ pipenv update

- Ejecutar un comando en el entorno virtual sin lanzar un nuevo shell

        $ pipenv run <comando>

    - Ejemplos:

            $ pipenv run django-admin startproject <nombre_proyecto>
            $ pipenv run python manage.py startapp <nombre_app>
            $ pipenv run python manage.py makemigrations
            $ pipenv run python manage.py migrate
            $ pipenv run python manage.py createsuperuser --email admin@example.com --username admin
            $ pipenv run python manage.py runserver

- Para transformar el archivo Pipfile en formato requirements.txt

        $ pipenv lock -r > requirements.txt

        $ pipenv lock -r -d > dev-requirements.txt

- Cuando todo funcione en desarrollo y se quiera pasar a producción. Se debe crear / actualizar el archivo Pipfile.lock ejecutando

        $ pipenv lock

> **Cuidado: Nunca se debe escribir manualmente información en el archivo Pipfile.lock.**


## Cómo levantar el proyecto usando venv (2):

- Crear el entorno virtual. En este caso se está usando la herramienta incluida de Python

        $ python3 -m venv env

- Activar el entorno virtual

        $ source env/bin/activate

- Instalar las dependencias del `requirements.txt` existente

        $ python3 -m pip install -r requirements.txt

- Levantar el servidor

        $ cd api

        $ python manage.py runserver

- Para desactivar el entorno virtual

        $ deactivate


## Despliegue en producción:

### En un servidor propio

- La instalación de dependencias se ejecuta mediante

        $ pipenv install --ignore-pipfile

    De modo que usa el archivo Pipfile.lock en vez de Pipfile.

- Para crear los archivos estáticos ejecutar

        $ python manage.py collectstatic --noinput --clear

- Actualizar las variables de entorno del archivo `.env`

- De ser necesario ejecutar la sincronización de la BD

        $ python manage.py migrate

- Levantar el servidor en el puerto deseado ejecutando

        $ gunicorn core.wsgi --bind 0.0.0.0:$PORT --error-logfile - --access-logfile - --workers 4

        **Nota:** de ser necesario agregar la bandera `--pythonpath api` a gunicorn o hacer `cd api/` antes de ejecutarlo.

### En un servidor de Heroku (3

**Referencias:**

(1) Documentación oficial de pipenv. https://pipenv.readthedocs.io/en/latest/index.html
(2) Documentación oficial de venv. https://docs.python.org/3/library/venv.html
(3) Configuring Django Apps for Heroku. https://devcenter.heroku.com/articles/django-app-configuration
