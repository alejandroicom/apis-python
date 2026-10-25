import os

import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise SystemExit("Falta GITHUB_TOKEN en el archivo .env")

session = requests.Session()
session.headers.update({
    "Accept": "application/vnd.github+json",
    "User-Agent": "apis-python-aprendizaje",
    "Authorization": f"Bearer {token}",
})

r = session.get("https://api.github.com/user", timeout=10)
r.raise_for_status()

yo = r.json()
print("Autenticado como:", yo["login"])
print("Límite de peticiones:", r.headers["X-RateLimit-Limit"])
print("Te quedan:", r.headers["X-RateLimit-Remaining"])