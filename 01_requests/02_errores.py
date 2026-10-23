import requests

BASE = "https://jsonplaceholder.typicode.com"


def obtener_usuario(user_id):
    try:
        respuesta = requests.get(f"{BASE}/users/{user_id}", timeout=10)
        respuesta.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"Error HTTP {respuesta.status_code} para el usuario {user_id}")
        return None
    except requests.exceptions.Timeout:
        print("El servidor tardó demasiado en responder")
        return None
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar (¿hay internet? ¿la URL es correcta?)")
        return None

    return respuesta.json()


for uid in [1, 999, 3]:
    usuario = obtener_usuario(uid)
    if usuario is None:
        continue

    print(usuario["name"])
    print("  Teléfono:", usuario.get("phone", "sin dato"))
    print("  Fax:", usuario.get("fax", "sin dato"))