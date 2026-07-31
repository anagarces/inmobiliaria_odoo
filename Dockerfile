ARG ODOO_VERSION=18.0
FROM odoo:${ODOO_VERSION}

USER root

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

USER odoo
