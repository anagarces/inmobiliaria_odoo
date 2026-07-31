# inmobiliariadoc_odoo

Entorno Docker para desarrollo de Odoo 18.0.

## Estructura

```
.
├── addons/                    Módulos custom (montado en /mnt/extra-addons)
├── config/odoo.conf.example   Plantilla de configuración de Odoo (versionada)
├── config/odoo.conf           Configuración real, con credenciales (NO versionado)
├── docker-compose.yml         Servicios: db (Postgres 15) y odoo
├── Dockerfile                 Imagen odoo:18.0 + dependencias de requirements.txt
├── requirements.txt           Dependencias Python adicionales para addons custom
├── .env.example               Plantilla de variables de entorno (versionada)
└── .env                       Variables de entorno reales (NO versionado)
```

## Primer arranque

1. Copiar el archivo de variables de entorno y ajustar `POSTGRES_PASSWORD`:
   ```bash
   cp .env.example .env
   ```

2. Copiar la plantilla de configuración de Odoo y fijar un `admin_passwd` propio (es la master password que permite crear/eliminar/restaurar bases de datos):
   ```bash
   cp config/odoo.conf.example config/odoo.conf
   ```
   Editar `admin_passwd` en `config/odoo.conf` con un valor fuerte y único.

3. Levantar los servicios:
   ```bash
   docker compose up -d --build
   ```

4. Abrir [http://localhost:8069](http://localhost:8069) y crear la base de datos desde el asistente inicial.

## Seguridad y credenciales

- `.env` y `config/odoo.conf` contienen credenciales reales y están en `.gitignore`: nunca deben commitearse. Solo se versionan sus plantillas (`.env.example`, `config/odoo.conf.example`).
- Antes de commitear, revisar con `git status` / `git diff --cached` que ninguno de los dos archivos reales aparezca en el staging area.
- Si algún secreto llega a commitearse, cambiar la credencial inmediatamente (rotar `admin_passwd` y `POSTGRES_PASSWORD`) y reescribir el historial de git para eliminarlo — cambiar el valor en un commit nuevo no lo borra del historial.
- En producción, considerar mover estas credenciales a un gestor de secretos (Docker secrets, Vault, variables de entorno del orquestador) en lugar de archivos locales.

## Comandos útiles

```bash
docker compose ps                     # Estado de los servicios
docker compose logs -f odoo           # Logs de Odoo
docker compose exec odoo bash         # Shell dentro del contenedor
docker compose restart odoo           # Reiniciar tras cambios en config/odoo.conf
docker compose down                   # Detener servicios (conserva volúmenes)
docker compose down -v                # Detener y borrar datos (Postgres + filestore)
```

## Añadir módulos custom

Colocar los módulos dentro de `addons/`. Ya están montados en `/mnt/extra-addons` y en el `addons_path` de `config/odoo.conf`. Tras añadir uno nuevo, actualizar la lista de apps desde Ajustes > Activar modo desarrollador > Actualizar lista de aplicaciones.

## Añadir dependencias Python

Agregar el paquete a `requirements.txt` y reconstruir la imagen:
```bash
docker compose up -d --build odoo
```
