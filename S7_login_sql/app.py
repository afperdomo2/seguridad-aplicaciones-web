import os
from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
import bcrypt
from dotenv import load_dotenv  # Importa load_dotenv


# Carga las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "sql_inyeccion_db"
app.config["MYSQL_DATABASE_HOST"] = "localhost"  # servidor MySQL
mysql = MySQL(app)

# Clave secreta para la sesión de Flask
app.secret_key = os.getenv(
    "SECRET_KEY"
)  # Carga la clave secreta desde la variable de entorno


# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")


# Ruta de registro de usuario
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode("utf-8")

        # Ciframos la contraseña antes de almacenarla
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cursor = mysql.get_db().cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password),
        )
        mysql.get_db().commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# Ruta de inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password_candidate = request.form["password"].encode("utf-8")

        cursor = mysql.get_db().cursor()
        cursor.execute(
            "SELECT id, username, password FROM users WHERE username = %s", (username,)
        )
        user = cursor.fetchone()

        if user:
            # Verificamos la contraseña cifrada
            if bcrypt.checkpw(password_candidate, user[2].encode("utf-8")):
                session["user_id"] = user[0]
                session["username"] = user[1]
                return redirect(url_for("dashboard"))

        error = "Inicio de sesión inválido"
        return render_template("login.html", error=error)

    return render_template("login.html")


# Ruta de dashboard después del inicio de sesión
@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        return render_template("dashboard.html")
    return redirect(url_for("login"))


# Ruta de cierre de sesión
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return render_template("logout.html")


if __name__ == "__main__":
    app.run(debug=True)
