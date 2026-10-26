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

# 1. Convertir texto a fecha
df["created_at"] = pd.to_datetime(df["created_at"])

# 2. Columnas calculadas
df["anio"] = df["created_at"].dt.year
df["antiguedad_dias"] = (pd.Timestamp.now(tz="UTC") - df["created_at"]).dt.days

# 3. Valores faltantes
print("Nulos por columna:")
print(df.isna().sum())
df["language"] = df["language"].fillna("Sin lenguaje")

# 4. Filtrar
activos = df[~df["archived"]]
print()
print(f"Activos: {len(activos)} de {len(df)}")

# 5. Agrupar
resumen = (
    activos.groupby("language")
    .agg(repos=("name", "count"), estrellas=("stargazers_count", "sum"), forks_promedio=("forks_count", "mean"))
    .round(1)
    .sort_values("repos", ascending=False)
)

creados = (
    df.groupby("anio")
    .agg(anio_count=("anio", "count"))
    .sort_values("anio", ascending=False)
)

print()
print(resumen)
print()
print(creados)
print()
print(df.dtypes)
print(df["created_at"].dtype)
