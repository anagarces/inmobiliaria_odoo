# inmobiliariadoc_odoo

Sistema de gestión inmobiliaria construido sobre Odoo 18.0, con entorno de desarrollo dockerizado. Permite publicar propiedades en venta, recibir y negociar ofertas de compradores, y factura automáticamente la venta al marcar una propiedad como vendida.

## Estructura

```
.
├── addons/
│   ├── estate/                 Módulo principal: propiedades, tipos, etiquetas, ofertas
│   └── estate_account/         Extiende estate: genera factura al vender una propiedad
├── config/odoo.conf.example    Plantilla de configuración de Odoo (versionada)
├── config/odoo.conf            Configuración real, con credenciales (NO versionado)
├── docker-compose.yml          Servicios: db (Postgres 15) y odoo
├── Dockerfile                  Imagen odoo:18.0 + dependencias de requirements.txt
├── requirements.txt            Dependencias Python adicionales para addons custom
├── .env.example                Plantilla de variables de entorno (versionada)
└── .env                        Variables de entorno reales (NO versionado)
```

## Módulos

### `estate` — Gestión inmobiliaria

Módulo principal (`depends: base`). Añade el menú **Real Estate** con las siguientes entidades:

**Modelos**

| Modelo | Descripción |
|---|---|
| `estate.property` | Una propiedad en venta (nombre, precio esperado, precio de venta, superficie, habitaciones, jardín, disponibilidad, etc.) |
| `estate.property.type` | Tipo de propiedad (Casa, Piso, ...), ordenable manualmente (`sequence`) |
| `estate.property.tag` | Etiquetas de propiedad (con color), nombre único |
| `estate.property.offer` | Oferta de compra sobre una propiedad, con validez y fecha límite calculada |
| `res.users` (extendido) | Añade `property_ids`: propiedades disponibles asignadas a un vendedor |

**Flujo de estados de una propiedad** (`state`): `new` → `offer_received` → `offer_accepted` → `sold`, con posibilidad de pasar a `cancelled` en cualquier punto salvo si ya está vendida.

**Reglas de negocio**

- Solo se puede eliminar una propiedad en estado `new` o `cancelled` (`_unlink_except_new_or_cancelled`).
- Una propiedad `cancelled` no puede marcarse como vendida, y una `sold` no puede cancelarse (botones **SOLD** / **CANCEL** en la ficha).
- El precio de venta no puede ser inferior al 90% del precio esperado (`_check_selling_price`).
- Al aceptar una oferta (`action_accept_offer`), la propiedad pasa a `offer_accepted`, se fija el comprador (`buyer_id`) y el precio de venta.
- Al crear una oferta, no se admite un precio inferior a la mejor oferta existente, y la propiedad pasa a `offer_received`.
- Campos calculados: `total_area` (superficie construida + jardín) y `best_price` (mejor oferta recibida).
- Al marcar `garden = True` desde el formulario, se rellenan automáticamente área y orientación del jardín (`onchange`).
- Nombres de tipos y etiquetas son únicos (`_sql_constraints`); precios de propiedad y oferta deben ser positivos.

**Vistas**: lista, kanban (agrupable por tipo, con colores según estado), formulario y búsqueda para propiedades; lista/formulario para tipos (con botón estadístico de nº de ofertas) y etiquetas; lista editable de ofertas embebida en la propiedad, con botones para aceptar/rechazar cada oferta.

### `estate_account` — Facturación de ventas

Módulo de integración (`depends: estate, account`). Sobrescribe `action_set_sold` en `estate.property`: al marcar una propiedad como vendida, genera automáticamente una factura de cliente (`account.move`, `out_invoice`) al comprador con dos líneas:

- Comisión de venta: 6% del precio de venta.
- Gastos administrativos: importe fijo de 100.

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

4. Abrir [http://localhost:8069](http://localhost:8069), crear la base de datos desde el asistente inicial, e instalar los módulos `estate` y `estate_account` desde Apps.

## Seguridad y credenciales

- `.env` y `config/odoo.conf` contienen credenciales reales y están en `.gitignore`: nunca deben commitearse. Solo se versionan sus plantillas (`.env.example`, `config/odoo.conf.example`).
- Antes de commitear, revisar con `git status` / `git diff --cached` que ninguno de los dos archivos reales aparezca en el staging area.
- Si algún secreto llega a commitearse, cambiar la credencial inmediatamente (rotar `admin_passwd` y `POSTGRES_PASSWORD`) y reescribir el historial de git para eliminarlo — cambiar el valor en un commit nuevo no lo borra del historial.
- En producción, considerar mover estas credenciales a un gestor de secretos (Docker secrets, Vault, variables de entorno del orquestador) en lugar de archivos locales.

## Comandos útiles

```bash
docker compose ps                     # Estado de los servicios
docker compose logs -f odoo           # Logs de Odoo (stdout; los errores de carga van al logfile, ver abajo)
docker compose exec odoo bash         # Shell dentro del contenedor
docker compose restart odoo           # Reiniciar tras cambios en config/odoo.conf o en modelos Python
docker compose down                   # Detener servicios (conserva volúmenes)
docker compose down -v                # Detener y borrar datos (Postgres + filestore)
```

Actualizar un módulo tras cambios de código (con el contenedor corriendo):
```bash
docker compose exec odoo odoo -c /etc/odoo/odoo.conf --db_host=db --db_port=5432 --db_user=odoo --db_password=<POSTGRES_PASSWORD> -d <nombre_bd> -u estate --stop-after-init --no-http
```
El `logfile` configurado en `odoo.conf` escribe en `/var/log/odoo/odoo.log` dentro del contenedor — revisar ahí (`docker compose exec odoo cat /var/log/odoo/odoo.log`) ante errores de instalación/actualización, ya que no siempre se reflejan en `docker compose logs`.

## Añadir módulos custom

Colocar los módulos dentro de `addons/`. Ya están montados en `/mnt/extra-addons` y en el `addons_path` de `config/odoo.conf`. Tras añadir uno nuevo, actualizar la lista de apps desde Ajustes > Activar modo desarrollador > Actualizar lista de aplicaciones.

## Añadir dependencias Python

Agregar el paquete a `requirements.txt` y reconstruir la imagen:
```bash
docker compose up -d --build odoo
```
