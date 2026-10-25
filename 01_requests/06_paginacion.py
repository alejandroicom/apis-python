import os
from collections import Counter

import requests
from dotenv import load_dotenv

load_dotenv()

session = requests.Session()
session.headers.update({
    "Accept": "application/vnd.github+json",
    "User-Agent": "apis-python-aprendizaje",
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
})


def obtener_todos(url, params=None):
    resultados = []
    pagina = 1

    while url:
        r = session.get(url, params=params, timeout=10)
        r.raise_for_status()
        yo = r.json()
 
        print("Límite de peticiones:", r.headers["X-RateLimit-Limit"])
        print("Te quedan:", r.headers["X-RateLimit-Remaining"])

        datos = r.json()
        resultados.extend(datos)
        print(f"Página {pagina}: {len(datos)} registros (total: {len(resultados)})")

        url = r.links.get("next", {}).get("url")
        params = None
        pagina += 1

    return resultados


repos = obtener_todos(
    "https://api.github.com/orgs/odoo/repos",
    params={"per_page": 10},
)

print()
print("Total de repos:", len(repos))



lenguajes = Counter(repo["language"] or "Sin lenguaje" for repo in repos)
print("Lenguajes más usados:")
for lenguaje, cantidad in lenguajes.most_common(5):
    print(f"  {lenguaje}: {cantidad}")


repo_max = max(repos, key=lambda repo: repo["stargazers_count"])

print("Repositorio:", repo_max["full_name"])
print("Max. estrellas:", repo_max["stargazers_count"])