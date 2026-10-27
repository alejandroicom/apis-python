import os
import requests
from dotenv import load_dotenv
import pandas as pd
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("__name__")

load_dotenv()

URL = os.getenv("ODOO_URL")

session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {os.getenv('ODOO_API_KEY')}",
    "X-Odoo-Database": os.getenv("ODOO_DB"),
    "User-Agent": "apis-python-aprendizaje",
})

def llamar(modelo, metodo, **parametros):

    r = session.post(f"{URL}/json/2/{modelo}/{metodo}", json=parametros, timeout=30)
    if not r.ok:
        try:
            detalle = r.json().get("message", r.text)
        except requests.exceptions.JSONDecodeError:
            detalle = r.text
        log.error("Error en %s/%s (HTTP %s): %s", modelo, metodo, r.status_code, detalle)
    r.raise_for_status()
    return r.json()
    

def upsert_contacto(datos, clave="vat"):
    """Crea el contacto si no existe; si existe, lo actualiza. Devuelve (id, accion)."""
    existentes = llamar(
        "res.partner", "search",
        domain=[[clave, "=", datos[clave]]],
        limit=2,
    )
    if len(existentes) > 1:
        raise ValueError(f"Hay más de un contacto con {clave}={datos[clave]}")
    if existentes:
        llamar("res.partner", "write", ids=existentes, vals=datos)
        return existentes[0], "actualizado"
    nuevo = llamar("res.partner", "create", vals_list=[datos])
    return nuevo[0], "creado"


res = upsert_contacto({
    "name": "Lalo Landa",
    "email": "prueba@ejemplo.com",
    "is_company": True,
    "city": "Salta",
    "vat": "20-12234567-6"
})

contacto_id = res[0]
accion = res[1]


print("ID:", contacto_id, "Acción:", accion)

llamar("res.partner", "write", ids=[contacto_id], vals={"phone": "+54 351 423416"})
print("Teléfono Actualizado")

leido = llamar("res.partner", "read", ids=[contacto_id], fields=["name", "city", "phone"])
print("Leído:", leido)

#llamar("res.partner", "unlink", ids=nuevo_id)
#print("Eliminado")

existe = llamar("res.partner", "search_count", domain=[["id", "in", [contacto_id]]])
print("¿Sigue existiendo?", existe)