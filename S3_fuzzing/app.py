from flask import Flask, request, render_template_string
import re

app = Flask(__name__)


# CREACIÓN DE LA RUTA PRINCIPAL: Maneja tanto solicitudes GET como POST
@app.route("/", methods=["GET", "POST"])
def home():
    error_message = None

    # Manejo de solicitudes POST
    if request.method == "POST":
        message = request.form["message"]
        cleaned_message = clean_input(message)
        # Limpieza de la entrada y renderización del resultado
        if cleaned_message is not None:
            return render_template_string(
                "Mensaje recibido: {{ message }}", message=cleaned_message
            )
        else:
            error_message = "Entrada no válida"

    # Renderización del formulario y manejo de errores
    return render_template_string(
        """
    <form method="post">
        <input type="text" name="message" placeholder="Escribe tu mensaje">
        <input type="submit" value="Enviar">
    </form>
    {% if error_message %}<p>{{ error_message }}</p>{% endif %}
    """,
        error_message=error_message,
    )


# Función de limpieza de entrada (para validar que la entrada solo contenga letras, números y espacios)
def clean_input(input_data):
    # Validar y limpiar la entrada para prevenir ataques de fuzzing
    if re.match(r"^[A-Za-z0-9\s]+$", input_data):
        cleaned_data = input_data.strip()
        return cleaned_data
    return None


if __name__ == "__main__":
    app.run()
