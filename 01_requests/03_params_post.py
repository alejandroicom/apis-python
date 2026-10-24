import requests

BASE = "https://jsonplaceholder.typicode.com"

# --- GET con parámetros: posts del usuario 1 ---
respuesta = requests.get(f"{BASE}/posts", params={"userId": 1}, timeout=10)
respuesta.raise_for_status()

print("URL final:", respuesta.url)

posts = respuesta.json()
print("Tipo:", type(posts), "- cantidad:", len(posts))

for post in posts[:3]:
    print(f"  #{post['id']}: {post['title']}")

print()

# --- POST: crear un post nuevo ---
nuevo = {
    "title": "Mi primer POST",
    "body": "Creado desde Python con requests",
    "userId": 1,
}

respuesta = requests.post(f"{BASE}/posts", json=nuevo, timeout=10)
respuesta.raise_for_status()

print("Status:", respuesta.status_code)
print("Respuesta:", respuesta.json())
print("Content-Type enviado:", respuesta.request.headers["Content-Type"])

respuesta = requests.put(f"{BASE}/posts/1", json={"title": "Mi primer PATCH"}, timeout=10)
respuesta.raise_for_status()
print("URL final:", respuesta.url)
print("Status:", respuesta.status_code)
print("Respuesta:", respuesta.json())

respuesta = requests.delete(f"{BASE}/posts/1", timeout=10)
respuesta.raise_for_status()
print("URL final:", respuesta.url)
print("Status:", respuesta.status_code)