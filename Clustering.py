import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler



def ObtenerDatos():
    df = pd.read_excel("37.-capac.-instalada-en-la-red-de-prest.-de-serv.-de-salud.xlsx")
    df = df[["Nombre del Prestador", "Grupo Capacidad", "Codigo Capacidad", "cantidad"]]
    df = df.dropna()

    df["GrupoCodigo"] = df["Grupo Capacidad"].astype("category").cat.codes
    df["prestador"] = df["Nombre del Prestador"]

    datos = df.to_dict(orient="records")
    return datos
def MetodoDelCodo():
    datos = ObtenerDatos()

    X = [
        [
            prestador["Codigo Capacidad"],
            prestador["cantidad"],
            prestador["GrupoCodigo"]
        ]
        for prestador in datos
    ]

    scaler = StandardScaler()
    xScaler = scaler.fit_transform(X)

    inercias = []
    valores_k = range(1, 11)

    for k in valores_k:
        modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
        modelo.fit(xScaler)
        inercias.append(modelo.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(valores_k, inercias, marker='o')
    plt.title("Método del Codo")
    plt.xlabel("Número de clusters (K)")
    plt.ylabel("Inercia")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/metodo_codo.png")
    plt.close()

    diferencias = []
    for i in range(1, len(inercias)):
        diferencias.append(inercias[i - 1] - inercias[i])

    k_optimo = 3

    for i in range(1, len(diferencias)):
        if diferencias[i] < diferencias[i - 1] * 0.5:
            k_optimo = i + 1
            break

    return k_optimo

def RealizarClustering(k):
    datos = ObtenerDatos()

    X = [
        [
            prestador["Codigo Capacidad"],
            prestador["cantidad"],
            prestador["GrupoCodigo"]
        ]
        for prestador in datos
    ]

    scaler = StandardScaler()
    xScaler = scaler.fit_transform(X)

    modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
    etiquetas = modelo.fit_predict(xScaler)

    resultados = []

    for i, prestador in enumerate(datos):
        fila = {
            "prestador": prestador["prestador"],
            "codigo_capacidad": prestador["Codigo Capacidad"],
            "cantidad": prestador["cantidad"],
            "grupo_capacidad": prestador["Grupo Capacidad"],
            "cluster": int(etiquetas[i])
        }
        resultados.append(fila)

    resumen_clusters = {}

    for etiqueta in etiquetas:
        etiqueta = int(etiqueta)
        resumen_clusters[etiqueta] = resumen_clusters.get(etiqueta, 0) + 1

    centroides = modelo.cluster_centers_

    return {
        "resultados": resultados,
        "resumen_clusters": resumen_clusters,
        "centroides": centroides,
        "k": k
    }

def GraficarClusters(cluster_filtrado=None):
    datos = ObtenerDatos()
    k = MetodoDelCodo()

    X = [
        [
            prestador["Codigo Capacidad"],
            prestador["cantidad"],
            prestador["GrupoCodigo"]
        ]
        for prestador in datos
    ]

    scaler = StandardScaler()
    xScaler = scaler.fit_transform(X)

    modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
    etiquetas = modelo.fit_predict(xScaler)

    centroides = modelo.cluster_centers_

    plt.figure(figsize=(9, 6))

    for cluster in range(k):
        if cluster_filtrado is not None and cluster != cluster_filtrado:
            continue

        xs = []
        ys = []

        for i in range(len(xScaler)):
            if etiquetas[i] == cluster:
                xs.append(xScaler[i][0])
                ys.append(xScaler[i][1])

        scatter = plt.scatter(xs, ys, label=f'Cluster {cluster}', alpha=0.6)

        plt.scatter(
            centroides[cluster][0],
            centroides[cluster][1],
            marker='X',
            s=250,
            color=scatter.get_facecolor()[0],
            edgecolors='black'
        )

    plt.xlabel("Código Capacidad (escalado)")
    plt.ylabel("Cantidad (escalado)")
    plt.title("Visualización de Clusters")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("static/clusters.png")
    plt.close()