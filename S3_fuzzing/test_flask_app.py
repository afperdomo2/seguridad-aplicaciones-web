# Importación de módulos
from flask import Flask, request
from flask.testing import FlaskClient
import re
from datetime import datetime

# Creación de la aplicación Flask
app = Flask(__name__)


# Definición de la ruta principal ('/') y función asociada:
@app.route("/", methods=["GET", "POST"])
def home():
    error_message = None
    # Manejo de solicitudes POST y registro en archivo
    if app.testing and request.method == "POST":
        message = request.form["message"]

        with open("registro.txt", "a") as f:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(
                f"{current_time} - Entrada: {message}\n"
            )  # Grabar la entrada en el archivo
            cleaned_message = clean_input(message)

            if cleaned_message is not None:
                app.logger.info(
                    f"Mensaje recibido con entrada válida: {cleaned_message}"
                )
                print(
                    "Mensaje recibido con entrada válida: " + cleaned_message
                )  # Agregar mensaje de salida en la terminal
                f.write(
                    f"{current_time} - Mensaje recibido con entrada válida: {cleaned_message}\n"
                )
                return f"Mensaje recibido: {cleaned_message}"
            else:
                error_message = "Entrada no válida"
                print("Entrada no válida")  # Agregar mensaje de salida en la terminal
                f.write(f"{current_time} - Entrada no válida: {message}\n")

    return "Aplicación Flask en modo de prueba"


# Función de limpieza de entrada (clean_input)
def clean_input(input_data):
    # Validar y limpiar la entrada para prevenir ataques de fuzzing
    if re.match(r"^[A-Za-z0-9\s]+$", input_data):
        cleaned_data = input_data.strip()
        print(
            "Validación de fuzzing ejecutada"
        )  # Agregar mensaje de salida en la terminal
        return cleaned_data
    return None


# Configuración de la aplicación en modo de prueba
if __name__ == "__main__":
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.post("/", data={"message": "e.nero 2024 $UNIMINUTO"})
