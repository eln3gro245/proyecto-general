from database import conexion as bd
import pymysql

#aqui es donde vamos buscar las predicciones para hacer envios de correos
def obtener_predicciones():
    try:
        prediccion_procesada = []
        conn = bd.conexion_db()

        #igual que en otros modulos usamos el with para habilitar el cursor 
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql_prediccion = """
                SELECT
                    m.nombre AS medicamento
                    p.cantidad_predicha AS cantidad_sugeridad
                    p.factor_climatico
                    p.probabilidad_alerta
                FROM predicciones_demanda p
                INNER JOIN medicamentos m ON p.id_medicamento = m.id_medicamento
                WHERE DATE(p.creado_el) = CURDATE();
            """
        cursor.execute(sql_prediccion)
        resultado = cursor.fetchall()

        for fila in resultado:
            motivo = f"Prediccion de demanda: {fila['probabilidad_alerta']}"
            if fila['factor_climatico'] != 'Normal':
                motivo += f"factor climatico: {fila['factor_climatico']}"
            
            prediccion_procesada.append({
                "medicamento": fila["medicamento"],
                "cantidad_sugerida": fila["cantidad_sugerida"],
                "motivo": motivo
            })

        return prediccion_procesada
    except Exception as e:
        print(f"Error al realizar consultas: {e}")
    finally:
        if conn:
            conn.close()
