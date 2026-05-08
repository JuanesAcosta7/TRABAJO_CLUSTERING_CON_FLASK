from flask import Flask,render_template, request
import Clustering
from Spark import obtener_resultados

app = Flask(__name__)

@app.route('/hello/')
def home():
    return 'Hello, World!'

@app.route('/')
def inicio():
    return render_template("index.html" )

@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

@app.route('/modelo')
def modelo():
    Clustering.MetodoDelCodo()
    return render_template('modelo.html')

@app.route('/resultados')
def resultados():
    cluster = request.args.get('cluster')
    k = Clustering.MetodoDelCodo()
    info = Clustering.RealizarClustering(k)
    if cluster is not None:
        cluster = int(cluster)
        Clustering.GraficarClusters(cluster)
        resultados_filtrados = [
            fila for fila in info["resultados"]
            if fila["cluster"] == cluster
        ]
        info["resultados"] = resultados_filtrados
    else:
        Clustering.GraficarClusters()
    return render_template(
        'resultados.html',
        info=info,
        cluster_actual=cluster
    )

@app.route('/interpretacion')
def interpretacion():
    return render_template('interpretacion.html')

@app.route('/spark')
def spark():
    resultados = obtener_resultados()

    return render_template(
        'ResSpark.html', 
         ventas_ciudad=resultados["ventas_ciudad"],
         ventas_categoria=resultados["ventas_categoria"],
         promedio_tienda=resultados["promedio_tienda"])