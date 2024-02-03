from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configura la conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="crud_app"
)
cursor = db.cursor()

# Ruta principal - Menú de opciones
#Rutas de la Aplicación:
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para listar registros
@app.route('/list')
def list():
    cursor.execute("SELECT * FROM registros")
    registros = cursor.fetchall()
    return render_template('list.html', registros=registros)

# Ruta para agregar un nuevo registro
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cursor.execute("INSERT INTO registros (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))
        db.commit()
        return redirect(url_for('list'))
    return render_template('add.html')

# Ruta para editar un registro
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cursor.execute("SELECT * FROM registros WHERE id = %s", (id,))
    registro = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cursor.execute("UPDATE registros SET nombre = %s, descripcion = %s WHERE id = %s", (nombre, descripcion, id))
        db.commit()
        return redirect(url_for('list'))
    
    return render_template('edit.html', registro=registro)

# Ruta para eliminar un registro
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM registros WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('list'))

#Ejecución de la Aplicación: inicia la aplicación Flask en modo de depuración
if __name__ == '__main__':
    app.run(debug=True)
