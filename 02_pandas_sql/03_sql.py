import sqlite3
import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

r = requests.get(
    "https://api.github.com/orgs/odoo/repos",
    params={"per_page": 100},
    headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
    timeout=10,
)
r.raise_for_status()

df = pd.DataFrame(r.json())

print("Filas y columnas:", df.shape)
print()

df = df[["name", "language", "stargazers_count", "forks_count", "created_at", "archived"]]
df["created_at"] = pd.to_datetime(df["created_at"])
df["anio"] = df["created_at"].dt.year
df["language"] = df["language"].fillna("Sin lenguaje")

conn = sqlite3.connect("github.db")

df.to_sql("repos", conn, if_exists="replace", index=False)
print("Guardados", len(df), "repos en la tabla 'repos'")
print()

consulta = """
    SELECT language,
           COUNT(*) AS repos,
           SUM(stargazers_count) AS estrellas
    FROM repos
    WHERE archived = 0
    GROUP BY language
    HAVING COUNT(*) >= 2
    ORDER BY repos DESC
"""
print(pd.read_sql(consulta, conn))
print()

anio_minimo = 2020
recientes = pd.read_sql(
    "SELECT name, anio, stargazers_count FROM repos WHERE anio >= ? ORDER BY anio",
    conn,
    params=(anio_minimo,),
)
print(recientes)

consulta = """
    SELECT name,
           forks_count
    FROM repos
    ORDER BY forks_count DESC
    LIMIT 3

"""
print(pd.read_sql(consulta, conn))
print()


resumen = (
    df[df["archived"] == False]
    .groupby("language")
    .agg(repos=("name", "count"), estrellas=("stargazers_count", "sum"))
    .sort_values(["repos","estrellas"], ascending=[False, False])
    .query("repos >= 2")
)

print (resumen)
print()

creados = (
    df.groupby("anio")
    .agg(anio_count=("anio", "count"))
    .sort_values("anio", ascending=False)
    
)

print()
print(creados)

conn.close()