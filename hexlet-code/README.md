<div align="center">

# Gestor de tareas

**Aplicación web para organizar el trabajo en equipo: usuarios, tareas, estados y etiquetas, con filtros y seguimiento de errores en producción.**

`Python 3.10+` · `Django` · `Bootstrap 5` · `PostgreSQL` · `uv` · `Render`

[**Ver la aplicación en producción**]("https://6d52a145b20645a297e384786e25b0f0@codexby.bugsink.com/1")

</div>

---

## Índice

- [Descripción](#descripción)
- [Funcionalidades](#funcionalidades)
- [Tecnologías](#tecnologías)
- [Modelo de datos](#modelo-de-datos)
- [Rutas](#rutas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación en local](#instalación-en-local)
- [Variables de entorno](#variables-de-entorno)
- [Comandos disponibles](#comandos-disponibles)
- [Pruebas](#pruebas)
- [Despliegue en Render](#despliegue-en-render)
- [Seguimiento de errores](#seguimiento-de-errores)
- [Autor](#autor)

---

## Descripción

Gestor de tareas es una aplicación web con renderizado del lado del servidor, construida con Django y Bootstrap 5. Permite registrar usuarios, crear tareas con un estado, un ejecutor y etiquetas, y encontrarlas rápidamente con filtros. Está desplegada en Render con PostgreSQL y notifica los errores de producción a un servicio de seguimiento.

## Funcionalidades

| Módulo | Qué permite |
| --- | --- |
| **Usuarios** | Registro, inicio y cierre de sesión, edición y eliminación de la propia cuenta. La lista de usuarios es pública. |
| **Estados** | CRUD de estados de tarea (nuevo, en progreso, en pruebas, terminado…). No se puede eliminar un estado en uso. |
| **Tareas** | CRUD con nombre, descripción, estado, ejecutor, etiquetas y autor. Solo el autor puede eliminar su tarea. |
| **Etiquetas** | CRUD de etiquetas con relación muchos a muchos con las tareas. No se puede eliminar una etiqueta asignada. |
| **Filtros** | Búsqueda de tareas por estado, ejecutor, etiqueta y «Solo mis tareas». |
| **Mensajes flash** | Avisos al crear, modificar o eliminar elementos. |
| **Errores en producción** | Notificación automática a Bugsink mediante el SDK de Sentry. |

Todas las secciones requieren sesión iniciada, salvo la lista de usuarios y el registro.

## Tecnologías

| Área | Herramientas |
| --- | --- |
| Lenguaje y framework | Python 3.12, Django |
| Gestor de dependencias | [uv](https://docs.astral.sh/uv/) |
| Interfaz | Bootstrap 5 con `django-bootstrap5` (sin CSS propio) |
| Filtros | `django-filter` |
| Configuración | `python-dotenv`, `dj-database-url` |
| Producción | `gunicorn`, `whitenoise`, PostgreSQL, Render |
| Monitorización | `sentry-sdk` (compatible con Bugsink) |
| Base de datos local | SQLite |

## Modelo de datos

| Modelo | Campos | Relaciones |
| --- | --- | --- |
| **User** | Modelo de usuario de Django | Es autor de muchas tareas y puede ser ejecutor de muchas tareas |
| **Status** | `name` (único), `created_at` | Un estado puede estar en muchas tareas |
| **Label** | `name` (único), `created_at` | Muchos a muchos con las tareas |
| **Task** | `name` (único), `description`, `created_at` | `author` (User), `executor` (User, opcional), `status` (Status) y `labels` (Label, varias) |

Las claves foráneas usan `PROTECT`: no se puede eliminar un usuario con tareas ni un estado en uso. Para las etiquetas, que son una relación muchos a muchos, la comprobación se hace en la vista.

## Rutas

<details>
<summary><strong>Ver todas las rutas</strong></summary>

<br>

| Ruta | Descripción | Acceso |
| --- | --- | --- |
| `/` | Página principal | Público |
| `/users/` | Lista de usuarios | Público |
| `/users/create/` | Registro | Público |
| `/users/<pk>/update/` | Editar usuario | Solo el propio usuario |
| `/users/<pk>/delete/` | Eliminar usuario | Solo el propio usuario |
| `/login/` | Iniciar sesión | Público |
| `/logout/` | Cerrar sesión (POST) | Sesión iniciada |
| `/statuses/` | Lista de estados | Sesión iniciada |
| `/statuses/create/` | Crear estado | Sesión iniciada |
| `/statuses/<pk>/update/` | Editar estado | Sesión iniciada |
| `/statuses/<pk>/delete/` | Eliminar estado | Sesión iniciada |
| `/tasks/` | Lista de tareas con filtros | Sesión iniciada |
| `/tasks/create/` | Crear tarea | Sesión iniciada |
| `/tasks/<pk>/` | Detalle de la tarea | Sesión iniciada |
| `/tasks/<pk>/update/` | Editar tarea | Sesión iniciada |
| `/tasks/<pk>/delete/` | Eliminar tarea | Solo el autor |
| `/labels/` | Lista de etiquetas | Sesión iniciada |
| `/labels/create/` | Crear etiqueta | Sesión iniciada |
| `/labels/<pk>/update/` | Editar etiqueta | Sesión iniciada |
| `/labels/<pk>/delete/` | Eliminar etiqueta | Sesión iniciada |
| `/admin/` | Panel de administración de Django | Administradores |

</details>

Parámetros del filtro de tareas: `status`, `executor`, `label` y `self_tasks`. Ejemplo: `/tasks/?status=1&self_tasks=on`.

## Estructura del proyecto

```text
hexlet-code/
├── manage.py
├── Makefile
├── build.sh
├── pyproject.toml
├── uv.lock
└── task_manager/
    ├── settings.py
    ├── urls.py
    ├── views.py          # Inicio, login y logout
    ├── mixins.py         # AuthRequiredMixin
    ├── templates/        # base.html, index.html y una carpeta por módulo
    ├── users/
    ├── statuses/
    ├── labels/
    └── tasks/            # Modelos, formularios, filtros, vistas y pruebas
```

---

## Instalación en local

> **Requisitos:** Python 3.10 o superior (lo gestiona `uv`), Git y `make`. En Windows se recomienda trabajar dentro de **WSL (Ubuntu)**. Si usas Linux o macOS, empieza en el [paso 2](#2-instalar-las-herramientas).

### 1. Preparar WSL (solo Windows)

En **PowerShell como administrador**:

```powershell
wsl --install -d Ubuntu
```

Reinicia si te lo pide y crea tu usuario y contraseña de Ubuntu. Comprueba que usa WSL 2:

```powershell
wsl -l -v
```

Instala **Visual Studio Code** en Windows, con la extensión **WSL** de Microsoft. A partir de aquí, todos los comandos se ejecutan en la **terminal de Ubuntu** (el prompt se parece a `usuario@PC:~$`), no en PowerShell.

> [!IMPORTANT]
> Trabaja siempre dentro del sistema de archivos de Linux (`~/`) y no en `/mnt/c/...` ni `/mnt/d/...`. Es más rápido y evita errores de permisos y de SQLite.

### 2. Instalar las herramientas

```bash
sudo apt update && sudo apt install -y git make curl build-essential libpq-dev dos2unix
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv --version
```

Para fijar una versión de Python (3.10 o superior):

```bash
uv python install 3.12
```

### 3. Clonar el repositorio

```bash
cd ~
git clone https://github.com/ByronDakFox/python-project-208.git
cd TU_REPOSITORIO/hexlet-code
ls
```

Debes ver `manage.py`, `Makefile` y `build.sh`. Si el proyecto está en la raíz del repositorio, entra solo a `TU_REPOSITORIO`.

### 4. Instalar las dependencias

```bash
make install
```

Ejecuta `uv sync`, que crea el entorno virtual `.venv` e instala todo lo necesario.

> [!TIP]
> Si existe un `.venv` creado desde Windows (con una carpeta `Scripts` en lugar de `bin`), bórralo y vuelve a instalar: `rm -rf .venv && make install`.

### 5. Crear el archivo `.env`

Junto a `manage.py`:

```bash
printf "DEBUG=True\nSECRET_KEY=cualquier-cadena-larga-para-local\n" > .env
```

Con `DEBUG=True` verás los errores detallados en el navegador. No añadas `DATABASE_URL` ni `SENTRY_DSN` en local: sin ellos se usa SQLite y no se envía nada al servicio de errores. El `.env` no debe subirse al repositorio.

### 6. Preparar la base de datos

```bash
make migrate
```

Debe mostrar una lista de líneas `Applying ... OK`.

### 7. Crear un administrador (opcional)

```bash
uv run python manage.py createsuperuser
```

Sirve para entrar en `/admin/`.

### 8. Arrancar el servidor

```bash
make dev
```

La aplicación queda disponible en <http://localhost:8000/>. El aviso «This is a development server» es normal. Para detener el servidor, pulsa `Ctrl+C`.

### 9. Ejecutar las pruebas

```bash
make test
```

### 10. Crear datos de ejemplo

Para poder crear tareas necesitas al menos un estado:

```bash
uv run python manage.py shell
```

```python
from task_manager.statuses.models import Status

for name in ['nuevo', 'en progreso', 'en pruebas', 'terminado']:
    Status.objects.get_or_create(name=name)
```

Sal con `exit()`. También puedes crearlos desde la web, en `/statuses/`, con la sesión iniciada.

<details>
<summary><strong>Problemas frecuentes</strong></summary>

<br>

| Síntoma | Causa y solución |
| --- | --- |
| `chmod` no se reconoce como comando | Estás en PowerShell. Abre la terminal de Ubuntu. |
| `No such file or directory: build.sh` | Estás en la carpeta equivocada. Entra a `hexlet-code` y comprueba con `ls`. |
| `make: *** missing separator` | El `Makefile` tiene espacios en lugar de tabuladores. Las líneas de comandos deben empezar con tabulador. |
| `bad interpreter` al ejecutar `build.sh` | Saltos de línea de Windows. Ejecuta `dos2unix build.sh Makefile`. |
| `table ... already exists` al migrar | La base local quedó a medias. Es de desarrollo: `rm db.sqlite3 && make migrate`. |
| `Server Error (500)` en local | Revisa que el `.env` tenga `DEBUG=True` y mira el traceback en la terminal de `make dev`. |
| `TemplateDoesNotExist` | La carpeta `task_manager/templates/` no coincide con `TEMPLATES['DIRS']` en `settings.py`. |
| Aviso `No directory at: .../staticfiles/` | Es inofensivo. Desaparece tras ejecutar `make collectstatic`. |

</details>

---

## Variables de entorno

| Variable | Uso | Obligatoria |
| --- | --- | --- |
| `SECRET_KEY` | Clave secreta de Django | En producción |
| `DEBUG` | `True` solo en desarrollo; por defecto `False` | No |
| `DATABASE_URL` | URL de PostgreSQL; si no existe, se usa SQLite | En producción |
| `SENTRY_DSN` | DSN del servicio de errores; si no existe, no se envía nada | En producción |
| `RENDER_EXTERNAL_HOSTNAME` | La define Render; se usa para `CSRF_TRUSTED_ORIGINS` | La pone Render |

> [!WARNING]
> Nunca subas el `.env`, claves ni el DSN al repositorio.

## Comandos disponibles

| Comando | Qué hace |
| --- | --- |
| `make install` | Instala las dependencias con `uv sync` |
| `make dev` | Arranca el servidor de desarrollo |
| `make migrate` | Aplica las migraciones |
| `make collectstatic` | Reúne los archivos estáticos |
| `make test` | Ejecuta las pruebas |
| `make build` | Ejecuta `build.sh` (lo usa Render) |
| `make render-start` | Arranca la app con gunicorn (lo usa Render) |

## Pruebas

```bash
make test
```

La batería cubre:

- El CRUD de usuarios, estados, tareas y etiquetas.
- Los permisos: acceso solo con sesión, edición de la propia cuenta y eliminación de tareas solo por su autor.
- El bloqueo al eliminar usuarios, estados y etiquetas en uso.
- Los filtros de tareas por estado, ejecutor, etiqueta y autor.

---

## Despliegue en Render

1. Sube el repositorio a GitHub.
2. Crea una base de datos **PostgreSQL** en Render y copia su *Internal Database URL*.
3. Crea un **Web Service** conectado al repositorio:

   | Ajuste | Valor |
   | --- | --- |
   | Root Directory | `hexlet-code` (solo si el proyecto está en un subdirectorio) |
   | Build Command | `make build` |
   | Start Command | `make render-start` |

4. En **Environment**, añade `DATABASE_URL`, `SECRET_KEY`, `SENTRY_DSN` y, opcionalmente, `WEB_CONCURRENCY`.
5. Despliega. Render vuelve a desplegar con cada push a la rama principal.

El archivo `build.sh` instala `uv` y ejecuta `make install && make collectstatic && make migrate`.

## Seguimiento de errores

La aplicación usa el SDK de Sentry, compatible con [Bugsink](https://www.bugsink.com/). La integración está en `task_manager/settings.py`:

```python
SENTRY_DSN = os.getenv('SENTRY_DSN')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment='production',
        send_default_pii=True,
        max_request_body_size='always',
    )
```

- El DSN se lee de la variable de entorno `SENTRY_DSN` y **nunca se guarda en el repositorio**.
- Los eventos se asocian al entorno `production`.
- Si la variable no existe (por ejemplo, en local), no se envía nada.

### Configurar el servicio

1. Crea una cuenta en Bugsink y un proyecto de tipo **Django**.
2. Copia el **DSN** del proyecto (tiene una forma parecida a `https://clave@tu-instancia.bugsink.com/1`).
3. En Render, abre el **Web Service** → **Environment** → **Add Environment Variable**:

   | Key | Value |
   | --- | --- |
   | `SENTRY_DSN` | El DSN copiado |

4. Guarda. Render vuelve a desplegar el servicio para que reciba la variable. Si no lo hace, usa **Manual Deploy → Deploy latest commit**.

### Cómo provocar un error controlado

Sirve para comprobar que los errores llegan al servicio. Es un mecanismo **temporal**: hay que eliminarlo al terminar.

**Paso 1. Añadir una ruta que falle.** En `task_manager/urls.py`:

```python
def trigger_error(request):
    return 1 / 0


urlpatterns = [
    path('sentry-debug/', trigger_error),
    # ...el resto de rutas igual
]
```

**Paso 2. Subir el cambio:**

```bash
git add .
git commit -m "Temporary: trigger test error"
git push
```

**Paso 3. Esperar al despliegue.** Espera a que el servicio aparezca como *Live*. En el plan gratuito, la primera petición tras un rato de inactividad puede tardar bastante.

**Paso 4. Provocar el error.** Abre en el navegador:

```text
https://TU-APP.onrender.com/sentry-debug/
```

Verás **Server Error (500)**. Es lo esperado: en producción `DEBUG` es `False` y Django no muestra el detalle.

**Paso 5. Comprobar que llegó al servicio.** Entra en Bugsink y abre el proyecto. Debe aparecer un `ZeroDivisionError` con el entorno `production`. Puede tardar unos segundos.

**Paso 6. Eliminar el mecanismo de prueba.** Borra la función `trigger_error` y la ruta `sentry-debug/` de `task_manager/urls.py` y sube el cambio:

```bash
git add .
git commit -m "Remove test error"
git push
```

<details>
<summary><strong>Si el error no aparece en el servicio</strong></summary>

<br>

- Comprueba que la variable se llama exactamente `SENTRY_DSN`, sin espacios, y que el DSN está completo (incluido el número final del proyecto).
- Revisa los logs de Render tras el despliegue. Un `ModuleNotFoundError: sentry_sdk` indica que faltó subir `pyproject.toml` y `uv.lock` con la dependencia.
- Confirma que el despliegue terminó y que usas la URL de tu servicio.
- Verifica que en Bugsink estás mirando el proyecto correcto.

</details>

<details>
<summary><strong>Probarlo en local (opcional)</strong></summary>

<br>

Añade temporalmente el DSN al `.env`, arranca con `make dev` y abre `http://localhost:8000//` con la ruta de prueba activa. Con `DEBUG=True` verás la página de error de Django y, además, el evento llegará al servicio con el entorno `production`, porque está fijado en el código. Al terminar, quita el DSN del `.env` y borra la ruta de prueba.

</details>

---

## Autor

**Byron Ramírez**

---

<div align="center">

Proyecto desarrollado como parte del curso de Python de [Hexlet](https://hexlet.io/).

</div>