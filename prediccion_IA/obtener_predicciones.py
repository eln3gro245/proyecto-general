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
                WITH UltimasPredicciones AS (
                    SELECT 
                        id_medicamento, 
                        cantidad_predicha, 
                        factor_climatico, 
                        ROW_NUMBER() OVER (PARTITION BY id_medicamento ORDER BY id_prediccion DESC) as rn
                    FROM predicciones_demanda
                )
                SELECT 
                    m.nombre AS medicamento,
                    SUM(p.cantidad_predicha) AS cantidad_sugerida,
                    MAX(p.factor_climatico) AS factor_climatico
                FROM UltimasPredicciones p
                INNER JOIN medicamentos m ON p.id_medicamento = m.id_medicamento
                WHERE p.rn <= 7
                GROUP BY m.id_medicamento, m.nombre;
            """
            cursor.execute(sql_prediccion)
            resultado = cursor.fetchall()

            for fila in resultado:
                cantidad_total = int(fila['cantidad_sugerida'])
                
                if cantidad_total > 350:
                    alerta = 'ALTA'
                elif cantidad_total > 210:
                    alerta = 'MEDIA'
                else:
                    alerta = 'BAJA'

                motivo = f"Alerta Semanal: {alerta}"
                if fila['factor_climatico'] != 'Normal':
                    motivo += f" (Clima: {fila['factor_climatico']})"
                
                prediccion_procesada.append({
                    "medicamento": fila["medicamento"],
                    "cantidad_sugerida": cantidad_total,
                    "motivo": motivo
                })

        return prediccion_procesada
    except Exception as e:
        print(f"Error al realizar consultas: {e}")
    finally:
        if conn:
            conn.close()
