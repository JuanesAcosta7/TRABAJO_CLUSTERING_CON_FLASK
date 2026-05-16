from flask import Flask, render_template, request
from Spark import obtener_resultados

# 🔥 CORRECTO (antes tenías _name_)
app = Flask(__name__)


@app.route('/hello/')
def home():
    return 'Hello, World!'


@app.route('/')
def spark_route():
    resultados = obtener_resultados()

    return render_template(
        'ResSpark.html',
        ventas_ciudad=resultados["ventas_ciudad"],
        ventas_categoria=resultados["ventas_categoria"],
        promedio_tienda=resultados["promedio_tienda"]
    )



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
    