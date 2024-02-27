import requests

# URL de la API
url = "https://jsonplaceholder.typicode.com/posts/1"

# Realizar una solicitud GET
response = requests.get(url)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Obtener los datos de la respuesta en formato JSON
    data = response.json()

    # Imprimir los datos
    print("Título del post:", data["title"])
    print("Cuerpo del post:", data["body"])
else:
    print("La solicitud GET no fue exitosa. Código de estado:", response.status_code)
