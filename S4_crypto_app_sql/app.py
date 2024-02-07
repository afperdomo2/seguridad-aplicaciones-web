import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from cryptography.fernet import Fernet

app = Flask(__name__)

# Configuración de la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="crypto_db"
)

cursor = db.cursor()

# Generar una clave Fernet
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener el mensaje del formulario
        original_message = request.form['message']

        # Cifrar el mensaje
        encrypted_message = cipher_suite.encrypt(original_message.encode()).decode()

        # Almacenar el mensaje cifrado en la base de datos
        #marcadores de posición: %s
        insert_query = "INSERT INTO messages (original_message, encrypted_message) VALUES (%s, %s)"
        data = (original_message, encrypted_message)
        cursor.execute(insert_query, data)
        db.commit()

        return redirect(url_for('messages'))
    
    return render_template('index.html')

@app.route('/messages')
def messages():
    # Obtener todos los mensajes almacenados
    cursor.execute("SELECT original_message, encrypted_message FROM messages")
    messages = cursor.fetchall()
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
