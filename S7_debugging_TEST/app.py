from flask import Flask, request, render_template, redirect, jsonify
from debugger import Debugger
import subprocess
import json

app = Flask(__name__)

# Lista para almacenar las personas y sus países
personas = []

# Crea una instancia del Debugger
debugger = Debugger()


# Función para cargar registros desde el archivo JSON al inicio
def cargar_registros_desde_json():
    try:
        with open("registros.json", "r") as json_file:
            registros = json.load(json_file)
            return registros
    except FileNotFoundError:
        return []


# Cargar registros al iniciar la aplicación
personas = cargar_registros_desde_json()


@app.route("/")
def index():
    debugger.log("Se cargó la página de inicio")  # Ejemplo de registro
    return render_template("index.html", personas=personas)


@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form.get("nombre").upper()  # Convertir el nombre a mayúsculas
    pais = request.form.get("pais")
    personas.append({"nombre": nombre, "pais": pais})
    guardar_registros_en_json(personas)
    debugger.log(f"Se registró a {nombre} desde {pais}")
    return redirect("/")


# Ruta para cargar los registros en formato JSON
@app.route("/personas_json")
def cargar_personas_json():
    return jsonify(personas)


# Función para guardar los registros en un archivo JSON
def guardar_registros_en_json(registros):
    with open("registros.json", "w") as json_file:
        json.dump(registros, json_file)


if __name__ == "__main__":
    app.run(debug=True)
