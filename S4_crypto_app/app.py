#importaciones
from flask import Flask, render_template, request
from cryptography.fernet import Fernet

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Generar una clave
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)

        # Obtener el mensaje del formulario
        message = request.form['message'].encode()

        # Cifrar el mensaje
        encrypted_message = cipher_suite.encrypt(message)

        return render_template('index.html', original_message=message.decode(), encrypted_message=encrypted_message.decode())
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
