from flask import Flask, render_template, request, url_for
import mysql.connector
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# La conexión a la base de datos de nuestro MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="encuesta_tecnologia"
)
cursor = conexion.cursor()

# La ruta principal donde nos muestra el encuesta.
@app.route('/')
def Encuesta():
    return render_template('Encuesta.html')

# La ruta para procesar nuestra encuesta.
@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form['nombre']
    edad = request.form['edad']
    direccion = request.form['direccion']
    sistema_operativo = request.form['sistema_operativo']
    red_social = request.form['red_social']
    nube = request.form['usa_nube']
    frecuencia = request.form['frecuencia']
    comentario = request.form['comentario']

    consulta = """
    INSERT INTO respuestas (nombre, edad, direccion, sistema_operativo, red_social_preferida, usa_nube, frecuencia_compra, comentario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    datos = (nombre, edad, direccion, sistema_operativo, red_social, nube, frecuencia, comentario)
    cursor.execute(consulta, datos)
    conexion.commit()

    return render_template('gracias.html')

# la ruta para mostrar la estadística de mi encuesta.
@app.route('/estadisticas')
def estadisticas():
    cursor.execute("SELECT sistema_operativo FROM respuestas")
    datos = cursor.fetchall()

    conteo = {}
    for (so,) in datos:
        conteo[so] = conteo.get(so, 0) + 1

    sistemas = list(conteo.keys())
    valores = list(conteo.values())

    # Aquí nos crea el gráfico de la encuesta.
    plt.bar(sistemas, valores, color="skyblue")
    plt.title("Sistema Operativo más Usado")
    plt.xlabel("Sistema Operativo")
    plt.ylabel("Cantidad de Usuarios")
    plt.grid(True, axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    os.makedirs("static", exist_ok=True)
    plt.savefig("static/grafico.png")
    plt.close()

    return render_template('estadisticas.html')

if __name__ == '__main__':
    app.run(debug=True)
