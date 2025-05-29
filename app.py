from flask import Flask, render_template, request
import mysql.connector
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Conexión a la base de datos usando variables de entorno
conexion = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASSWORD", "admin"),
    database=os.environ.get("DB_NAME", "encuesta_tecnologia")
)
cursor = conexion.cursor()

# Ruta principal
@app.route('/')
def encuesta():
    return render_template('Encuesta.html')

# Ruta para procesar la encuesta
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
        INSERT INTO respuestas (
            nombre, edad, direccion,
            sistema_operativo, red_social_preferida,
            usa_nube, frecuencia_compra, comentario
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    datos = (nombre, edad, direccion, sistema_operativo, red_social, nube, frecuencia, comentario)
    cursor.execute(consulta, datos)
    conexion.commit()

    return render_template('gracias.html')

# Ruta de estadísticas
@app.route('/estadisticas')
def estadisticas():
    cursor.execute("SELECT sistema_operativo FROM respuestas")
    datos = cursor.fetchall()

    conteo = {}
    for (so,) in datos:
        conteo[so] = conteo.get(so, 0) + 1

    sistemas = list(conteo.keys())
    valores = list(conteo.values())

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
