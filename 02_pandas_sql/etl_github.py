import logging
import os
import sqlite3
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

log = logging.getLogger(__name__)

COLUMNAS = ["name", "language", "stargazers_count", "forks_count", "created_at", "archived"]



def extraer(org,max_paginas=None, por_pagina=100, max_reintentos=3):
    """Trae los repos públicos de una organización de GitHub."""

    reintentos = Retry(
    total=max_reintentos,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
    )
    
    params = {"per_page": por_pagina}
   
    load_dotenv()

    session = requests.Session()
    session.headers.update({
        "Accept": "application/vnd.github+json",
        "User-Agent": "apis-python-aprendizaje",
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    })
    session.mount("https://", HTTPAdapter(max_retries=reintentos))

    url = (f"https://api.github.com/orgs/{org}/repos")
    resultados = []
    pagina = 1
    while url:
        try:
            r = session.get(url, params=params, timeout=10)
            r.raise_for_status()

            restantes = int(r.headers["X-RateLimit-Remaining"])
            log.debug("Rate limit: quedan %d de %s", restantes, r.headers["X-RateLimit-Limit"])
            if restantes < 100:
                log.warning("Quedan solo %d peticiones disponibles", restantes)
            datos = r.json()
            resultados.extend(datos)
        
            log.info("Extraídos %d repos de página %s de %s", len(datos), pagina, org)
            url = r.links.get("next", {}).get("url")
            params = None
            pagina += 1

            if max_paginas is not None and pagina > max_paginas:
                log.warning("Se alcanzó el límite de páginas (%d). Deteniendo la extracción.", max_paginas)
                break
        except requests.exceptions.RequestException:
            log.error("Falló la extracción de %s en la página %d", org, pagina)
            raise



    log.info("Extraído un total de %s repos de %s", len(resultados) , org)       

       
    return resultados


def transformar(datos):
    """Convierte el JSON crudo en un DataFrame limpio."""
    df = pd.DataFrame(datos)[COLUMNAS]
    
    df["created_at"] = (
        pd.to_datetime(df["created_at"],utc=True)
        .dt.tz_convert("America/Argentina/Buenos_Aires")
        .dt.tz_localize(None)
    )

    df["anio"] = df["created_at"].dt.year
    df["language"] = df["language"].fillna("Sin lenguaje")
    log.info("Transformados %d registros", len(df))
    return df


def cargar(df, ruta_db, tabla):
    """Guarda el DataFrame en una tabla SQLite."""
    with sqlite3.connect(ruta_db) as conn:
        df.to_sql(tabla, conn, if_exists="replace", index=False)
    log.info("Cargados %d registros en %s.%s", len(df), ruta_db, tabla)

def consultar(ruta_db, sql, params=None, parse_dates=None):
    """Ejecuta una consulta SQL y devuelve un DataFrame."""
    with sqlite3.connect(ruta_db) as conn:
        return pd.read_sql_query(sql, conn, parse_dates=parse_dates, params=params)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    datos = extraer("odoo")
    df = transformar(datos)
    cargar(df, "github.db", "repos")