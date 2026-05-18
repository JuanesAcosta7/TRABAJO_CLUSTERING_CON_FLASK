from flask import Flask, render_template, request
from Spark import obtener_resultados
import time


app = Flask(__name__)


@app.route('/hello/')
def home():
    return 'Hello, World!'


@app.route('/')
def spark_route():
    inicio = time.time()

    resultados = obtener_resultados()

    fin = time.time()

    print("Tiempo de ejecución:", fin - inicio, "segundos")


    return render_template(
        'ResSpark.html',
        ventas_ciudad=resultados["ventas_ciudad"],
        ventas_categoria=resultados["ventas_categoria"],
        promedio_tienda=resultados["promedio_tienda"]
    )



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
    