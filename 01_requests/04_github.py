import requests

session = requests.Session()
session.headers.update({
    "Accept": "application/vnd.github+json",
    "User-Agent": "apis-python-aprendizaje",
})

BASE = "https://api.github.com"


def get(ruta, **kwargs):
    respuesta = session.get(f"{BASE}{ruta}", timeout=10, **kwargs)
    respuesta.raise_for_status()
    return respuesta


r = get("/users/alejandroicom")
perfil = r.json()
print("Usuario:", perfil["login"])
print("Repos públicos:", perfil["public_repos"])
print("Creado:", perfil["created_at"])
print()

r = get("/users/alejandroicom/repos", params={"sort": "updated", "per_page": 5})
for repo in r.json():
    print(f"  {repo['name']} - {repo.get('language') or 'sin lenguaje'}")
print()

print("Límite de peticiones:", r.headers["X-RateLimit-Limit"])
print("Te quedan:", r.headers["X-RateLimit-Remaining"])