from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="crud_app"
)
#objeto que permite interactuar con un conjunto de resultados de una consulta SQL
# El cursor actúa como un apuntador o marcador de posición que permite navegar y manipular los resultados de una consulta.
cursor = db.cursor()

#Rutas de la Aplicación:
@app.route('/')
def index():
    return render_template('index.html')

#Ruta para realizar una búsqueda (/search):
@app.route('/search', methods=['POST'])
def search():
    # Obtén el término de búsqueda del formulario
    search_term = request.form['search_term']

    # Consulta parametrizada para prevenir inyecciones SQL
    query = "SELECT * FROM registros WHERE nombre = %s"  # %s: consultas parametrizadas o consultas preparadas
    cursor.execute(query, (search_term,))

    # Obtiene los resultados de la consulta
    results = cursor.fetchall()

    return render_template('results.html', results=results)

#Ejecución de la Aplicación:Se inicia la aplicación Flask en modo de depuración
if __name__ == '__main__':
    app.run(debug=True)
