# inmobiliariadoc_odoo

Entorno Docker para desarrollo de Odoo 18.0.

## Estructura

```
.
├── addons/             Módulos custom (montado en /mnt/extra-addons)
├── config/odoo.conf    Configuración de Odoo
├── docker-compose.yml  Servicios: db (Postgres 15) y odoo
├── Dockerfile          Imagen odoo:18.0 + dependencias de requirements.txt
├── requirements.txt    Dependencias Python adicionales para addons custom
└── .env                Variables de entorno (no versionado, ver .env.example)
```

## Primer arranque

1. Copiar el archivo de variables de entorno:
   ```bash
   cp .env.example .env
   ```
   Ajustar `POSTGRES_PASSWORD` y `ADMIN_PASSWD` antes de usar en un entorno compartido.

2. Levantar los servicios:
   ```bash
   docker compose up -d --build
   ```

3. Abrir [http://localhost:8069](http://localhost:8069) y crear la base de datos desde el asistente inicial.

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
