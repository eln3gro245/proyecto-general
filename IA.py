from database import conexion as bd
import pandas as pd
import xgboost as xgb
import joblib
import pymysql

def obtener_datos():
    try:
        conn = bd.conexion_db()

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            #obtenemos los datos que usaremos para entrenar a la IA
            #usamos el pasado para entender el futuro
            sql = """
                SELECT 
                    l.id_medicamento,
                    WEEKDAY(h.fecha_hora) AS dia_semana,
                    MONTH(h.fecha_hora) AS mes,
                    h.cantidad AS cantidad_vendida,
                    CASE
                        WHEN MONTH(h.fecha_hora) IN (12, 1, 2) THEN 1 -- Estación 1 (Ej: Sequía / Comienzo de año)
                        WHEN MONTH(h.fecha_hora) IN (3, 4, 5) THEN 2  -- Estación 2 (Ej: Alta temperatura / Vientos)
                        WHEN MONTH(h.fecha_hora) IN (6, 7, 8) THEN 3  -- Estación 3 (Ej: Lluvias esporádicas)
                        WHEN MONTH(h.fecha_hora) IN (9, 10, 11) THEN 4 -- Estación 4 (Ej: Humedad / Fin de año)
                        END AS factor_climatico
                    FROM historial_movimientos h
                    JOIN lote_inventario l ON h.id_lote = l.id_lote
                    WHERE h.tipo_movimiento = 'Salida';
            """
            cursor.execute(sql)
            #convertimos el resultado en un dataframe de pandas para poder manipularlo y entrenar la IA
            estudio = pd.read_sql_query(sql, conn)

        return estudio
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
    finally:
        if conn:
            conn.close()

#lo hacemos de esta manera para que solo estudie cuando activamos este modulo para no saturar el servidor o la PC cuando se ejecuta fastapi
if __name__ == "__main__":
    datos = obtener_datos()
    print(datos.head())

    if datos is not None and not datos.empty:
        # el modelo necesita agrupar los datos para encontrar patrones, por eso separamos las variables independientes (X) de la dependiente (y)
        X = datos[['id_medicamento', 'dia_semana', 'mes', 'factor_climatico']]
        y = datos['cantidad_vendida']

        # aqui le decimos al modelo bajo que parametros se va a regir, como la cantidad de arboles que va a usar, la profundidad de los mismos y la tasa de aprendizaje
        modelo = xgb.XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        # ya aqui es donde el modelo se pone a estudiar con los datos que obtuvo
        modelo.fit(X, y)

        # Guardamos un archivo .pkl donde estara el modelo entrenado para que pueda ser usado en la aplicacion web
        joblib.dump(modelo, 'modelo_xgboost.pkl')
        print("Modelo entrenado y guardado como 'modelo_xgboost.pkl'")
