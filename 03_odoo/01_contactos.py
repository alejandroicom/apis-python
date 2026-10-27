import os
import requests
from dotenv import load_dotenv
import pandas as pd

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
    r.raise_for_status()
    return r.json()



dominio = [["is_company", "=", True], ["country_id.code", "=", "US"]]

empresas = llamar(
    "res.partner",
    "search_read",
    domain=dominio,
    fields=["name", "email", "city", "country_id", "is_company"],
    limit=5,
)

for e in empresas:
    print(e)

total = llamar("res.partner", "search_count", domain=dominio)
print("Total de empresas:", total)


def leer_todo(modelo, dominio, campos, tamanio_pagina=50):
    """Lee todos los registros que cumplen el dominio, paginando con offset."""
    resultados = []
    offset = 0
    while True:
        pagina = llamar(
            modelo, "search_read",
            domain=dominio, fields=campos,
            limit=tamanio_pagina, offset=offset, order="id",
        )
        resultados.extend(pagina)
        log_msg = f"offset {offset}: {len(pagina)} registros"
        print(log_msg)
        if len(pagina) < tamanio_pagina:
            break
        offset += tamanio_pagina
        
    return resultados



dominio =  [["state", "=", "sale"]]

pedidos = leer_todo(
    "sale.order",
    dominio,
    ["name", "partner_id", "date_order", "amount_total", "state"],
    tamanio_pagina=5,
)
print("Pedidos confirmados:", len(pedidos))
print("Control:", llamar("sale.order", "search_count", domain=dominio))
for p in pedidos[:3]:
    print(p)


df = pd.DataFrame(pedidos)

df["cliente_id"] = df["partner_id"].apply(lambda x: x[0] if isinstance(x, list) else None)
df["cliente"] = df["partner_id"].apply(lambda x: x[1] if isinstance(x, list) else None)
df = df.drop(columns="partner_id")

df["date_order"] = (
    pd.to_datetime(df["date_order"])
    .dt.tz_localize("UTC")
    .dt.tz_convert("America/Argentina/Buenos_Aires")
)

print(df)
