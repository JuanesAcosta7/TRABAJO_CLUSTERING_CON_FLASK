import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, desc

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

def get_spark_session():
    spark = SparkSession.builder \
        .appName("AnalisisVentasLocal") \
        .master("spark://10.40.1.97:7077") \
        .config("spark.driver.host", "127.0.0.1") \
        .config("spark.driver.bindAddress", "127.0.0.1") \
        .config("spark.ui.enabled", "false") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()
    
    return spark

def cargar_datos():
    spark = get_spark_session()
    df = spark.read.csv( "file:///C:/sparkpro/ventas.csv", header=True,
        inferSchema=True
        )
    df = df.withColumn("Total", col("cantidad") * col("precio_unitario"))

    return df

def obtener_resultados():
    df = cargar_datos()

    ventas_ciudad = df.groupBy("Ciudad").agg(sum("Total").alias("total_ventas")).orderBy(desc("total_ventas")).toPandas().to_dict(orient="records")
    ventas_categoria = (
    df.groupBy("categoria")
      .agg(sum("Total").alias("total_ventas"))
      .orderBy(desc("total_ventas"))
      .toPandas()
      .to_dict(orient="records")
    )
    promedio_tienda = df.groupBy("Tienda").agg(avg("Total").alias("promedio_venta")).orderBy(desc("promedio_venta")).toPandas().to_dict(orient="records")


    return {
        "ventas_ciudad": ventas_ciudad,
        "ventas_categoria": ventas_categoria,
        "promedio_tienda": promedio_tienda
    }