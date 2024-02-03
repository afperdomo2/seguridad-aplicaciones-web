from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector

app = Flask(__name__)
#Configuración de la aplicación y la clave secreta de la sesión
app.secret_key = 'your_secret_key' 

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="myapp_user"  # Nombre de la base de datos que creaste
)
#Rutas de la aplicación:
@app.route('/') #/: Esta ruta muestra la página de inicio. Si el usuario ha iniciado sesión, muestra un saludo personalizado; de lo contrario, muestra un mensaje y un enlace para iniciar sesión.
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return 'No has iniciado sesión. <a href="/login">Iniciar sesión</a>'

#Ruta de inicio de sesión (/login):
@app.route('/login', methods=['GET', 'POST']) 
#/login: Esta ruta maneja la página de inicio de sesión. Si se envía un formulario POST.  Si se accede a la página mediante GET, muestra el formulario de inicio de sesión.
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validación de entrada: Evita la inyección SQL
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Iniciar sesión
            session['username'] = user[1]
            return redirect(url_for('index'))

    return render_template('login.html')

#Ruta de cierre de sesión (/logout):
@app.route('/logout') #Esta ruta permite al usuario cerrar sesión y luego redirige a la página de inicio.
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

#Ejecución de la Aplicación:
if __name__ == '__main__':
    app.run(debug=True)
