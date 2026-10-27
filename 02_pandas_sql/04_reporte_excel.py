import logging
import pandas as pd

from etl_github import consultar

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("reporte")

DB = "github.db"

repos = consultar(DB, "SELECT * FROM repos ORDER BY stargazers_count DESC",params=None, parse_dates=["created_at"] )

por_lenguaje = consultar(DB, """
    SELECT language AS lenguaje,
           COUNT(*) AS repos,
           SUM(stargazers_count) AS estrellas,
           ROUND(AVG(forks_count), 1) AS forks_promedio
    FROM repos
    WHERE archived = 0
    GROUP BY language
    ORDER BY repos DESC, estrellas DESC
""")

por_anio = consultar(DB, """
    SELECT anio, COUNT(*) AS repos_creados
    FROM repos
    GROUP BY anio
    ORDER BY anio
""")

top10 = consultar(DB, """
    SELECT name, language, stargazers_count AS estrellas FROM repos 
    ORDER BY stargazers_count DESC
    LIMIT 10
""")



with pd.ExcelWriter("reporte_github.xlsx") as writer:
    por_lenguaje.to_excel(writer, sheet_name="Por lenguaje", index=False)
    por_anio.to_excel(writer, sheet_name="Por año", index=False)
    repos.to_excel(writer, sheet_name="Detalle", index=False)
    top10.to_excel(writer, sheet_name="Top 10", index=False)

log.info("Reporte generado: reporte_github.xlsx")


