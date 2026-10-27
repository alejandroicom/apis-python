from etl_github import extraer, transformar, cargar, consultar

import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

    
datos = extraer("microsoft", 
                max_paginas=3, 
                por_pagina=100)

print()

df = transformar(datos)

print()

cargar(df, "github.db", "repos")

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
print(consultar("github.db", consulta))
print()

anio_minimo = 2020
recientes = consultar("github.db", "SELECT name, anio, stargazers_count FROM repos WHERE anio >= ? ORDER BY anio", params=(anio_minimo,))
print(recientes)

consulta = """
    SELECT name,
           forks_count
    FROM repos
    ORDER BY forks_count DESC
    LIMIT 3

"""
print(consultar("github.db", consulta))
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

