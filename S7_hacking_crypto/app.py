from flask import Flask, request, render_template
from cryptography.fernet import Fernet, InvalidToken

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    mensaje_cifrado = ""
    mensaje_descifrado = ""

    if request.method == "POST":
        # Genera una clave de cifrado aleatoria cada vez que se recibe un mensaje
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)

        mensaje = request.form["mensaje"].encode()
        mensaje_cifrado = cipher_suite.encrypt(mensaje)

        try:
            mensaje_descifrado = cipher_suite.decrypt(mensaje_cifrado).decode()
        except InvalidToken:
            mensaje_descifrado = "Error al descifrar el mensaje"

    return render_template(
        "index.html",
        mensaje_cifrado=mensaje_cifrado,
        mensaje_descifrado=mensaje_descifrado,
    )


if __name__ == "__main__":
    app.run(debug=True)
