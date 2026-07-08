from datetime import datetime, timedelta
from database import conexion as db
import pandas as pd
import pymysql
import joblib

def generar_y_guerdar_predicciones_semanales():
    # antes que nada cargamos el modelo de IA que nosotros mismo entrenamos
    modelo = joblib.load('modelo_xgboots.pkl')

    fecha_actual = datetime.now()

    try:
        conn = db.conexion_db()
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # aqui es donde obtenemos los ID de los medicamentos 
            cursor.execute("SELECT id_medicamento FROM medicamentos")
            medicamentos = cursor.fetchall()

            for med in medicamentos:
                #aqui iteramos los medicamento para hacer las prediccones
                id_med = med['id_medicamento']

                #aqui predecimos de acuerdo a los proximos 7 dias
                for i in range(1 , 8):
                    fecha_futura = fecha_actual + timedelta(days=i)
                    dia_semana = fecha_futura.weekday()
                    mes = fecha_futura.month

                    #verificamos en que mes nos encontramos por que la prediccion toma en cuenta le factor climatico
                    if mes in [12, 1, 2]: factor_climatico = 1
                    elif mes in [3, 4, 5]: factor_climatico = 2
                    elif mes in [6, 7, 8]: factor_climatico = 3
                    else: factor_climatico = 4
                    #todos esta de acuerdo a lo hecho con el tema de la IA el clima y la base de datos

                    #creamos una variable con todo el esenaria hecho para que la IA pueda predicir el stock del medicamento
                    futuro = pd.DataFrame([{
                        'id_medicamento': id_med,
                        'dia_semana': dia_semana,
                        'mes': mes,
                        'factor_climatico': factor_climatico
                    }])

                    predicion_pura = modelo.predict(futuro)[0]
                    
                    #ahora obtenemos el resultado de su prediccion (hacemos uso de esas funcion devolver un numero entero positivo)
                    cantidad_predicha = max(0, round(predicion_pura))

                    #ahora preparamos los datos para guardarlos dentro de la base de datos para tener el registro de la prediccion
                    #definimos el tiempo cliamtico para la base de datos
                    if factor_climatico == 1: clima = 'Normal'
                    elif factor_climatico == 2: clima = 'Alta Temperatura'
                    elif factor_climatico == 3: clima = 'Temporada de Lluvias'
                    elif factor_climatico == 4: clima = 'Frente Frio'

                    #ahora tenemos la alerta critica de los medicamentos 
                    if cantidad_predicha > 50: alerta = 'ALTA'
                    elif cantidad_predicha > 30: alerta = 'MEDIA'
                    elif cantidad_predicha > 10: alerta = 'BAJA'

                    #ahora para terminar realizamos una consulta sql para guardar los datos de la base de datos
                    sql = """
                        INSERT INTO predicciones_demanda
                        (id_medicamento, fecha_prediccion, cantidad_predicha, factor_climatico, probabilidad_alerta)
                        VALUES(%s,%s,%s,%s,%s)
                    """

                    cursor.execute(sql, (id_med, fecha_futura.date(), cantidad_predicha, factor_climatico, alerta))

            conn.commit()
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
    finally:
        if conn:
            conn.close()

                    


    
