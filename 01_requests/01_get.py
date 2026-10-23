import requests

URL = "https://jsonplaceholder.typicode.com/users/1"

respuesta = requests.get(URL,timeout=10)

print ("Status: ", respuesta.status_code)
print("Content-Type: ", respuesta.headers['Content-Type'])
print()

usuario = respuesta.json()

print(usuario)
print("Tipo de dato: ", type(usuario))
print("Usuario: ", usuario['name'])
print("Email: ", usuario['email'])
print("Ciudad: ", usuario['address']['city'])
print("Compañía: ", usuario['company']['name'])

