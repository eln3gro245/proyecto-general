from database import conexion as bd
import pymysql 

#estas son la consultas que usaremos para la plantilla principal de inicio, para mostrar estadisticas y demas
def consultas_globales_principal():
    #administrar diccionario de retorno a fastapi
    stats = {
        "visitas": 0,
        "popularidad": "Ninguno",
        "eficiencia": "0%",
        "rotacion": 0.0,
        "mensaje_rotacion": "Sin alertas esta semana.",
        "rendimiento_descripcion": "Flujo de inventario estable."
    }

    try:
        conn = bd.conexion_db()
        
        #creamos el cursor usando conexion activa
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:

            # primera consulta: movimientos del dia
            sql_visitas = "SELECT COUNT(*) AS total FROM historial_movimientos WHERE DATE(fecha_hora) = CURDATE();"
            cursor.execute(sql_visitas)
            resultado_visitas = cursor.fetchone()
            if resultado_visitas:
                stats["visitas"] = resultado_visitas["total"]

            # segunda consulta: producto más popular o vendido
            sql_popular = """
                SELECT m.nombre
                FROM historial_movimientos h
                JOIN lote_inventario l ON h.id_lote = l.id_lote
                JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
                WHERE h.tipo_movimiento = 'Salida'
                GROUP BY m.id_medicamento, m.nombre
                ORDER BY COUNT(*) DESC
                LIMIT 1;
                    """
            cursor.execute(sql_popular)
            resultado_popular = cursor.fetchone()
            if resultado_popular:
                stats["popularidad"] = resultado_popular["nombre"]
            
            # tercera consulta: IA predictiva
            sql_ia = """
                SELECT m.nombre, p.cantidad_predicha, p.probabilidad_alerta, p.factor_climatico
                FROM predicciones_demanda p
                JOIN medicamentos m ON p.id_medicamento = m.id_medicamento
                ORDER BY id_prediccion DESC
                LIMIT 1;
                    """
            cursor.execute(sql_ia)
            resultado_ia = cursor.fetchone()
            if resultado_ia:
                med = resultado_ia["nombre"]
                can = resultado_ia["cantidad_predicha"]
                alerta = resultado_ia["probabilidad_alerta"]
                clima = resultado_ia["factor_climatico"]

                stats["rotacion"] = can
                stats["mensaje_rotacion"] = f"Alerta {alerta}: Se proyecta demanda de {can} unidades de {med}."
                stats["rendimiento_descripcion"] = f"Factor climático: {clima}. Ajuste de inventario recomendado."

            # cuarta consulta: rotacion de inventario
            sql_rotacion = """
                SELECT
                    (SELECT IFNULL(SUM(cantidad), 0) FROM historial_movimientos WHERE tipo_movimiento = 'Salida') /
                    (SELECT IFNULL(SUM(stock_actual), 1) FROM lote_inventario) AS indice_rotacion;
                    """
            cursor.execute(sql_rotacion)
            resultado_rotacion = cursor.fetchone()
            if resultado_rotacion:
                stats["rotacion"] = round(float(resultado_rotacion["indice_rotacion"]), 2)
            
            # quinta consulta: eficiencia del inventario
            sql_eficiencia = """
                SELECT IFNULL(
                            (SELECT COUNT(*) FROM historial_movimientos WHERE tipo_movimiento = 'Salida') /
                            COUNT(*) * 100, 
                            100
                            ) AS eficiencia
                            FROM historial_movimientos;
                    """
            cursor.execute(sql_eficiencia)
            resultado_eficiencia = cursor.fetchone()
            if resultado_eficiencia:
                stats["eficiencia"] = f"{round(resultado_eficiencia['eficiencia'], 1)}%"
            
        return stats

    except Exception as e:
        print(f"Error al ejecutar consultas globales: {e}")
    finally:
        if conn:
            conn.close()

def consultas_globales_auditoria():
    auditoria_data = {
        "ultima_sincronizacion": "No disponible",
        "registros_alterados": 0,
        "token_sesion": "S/T",
        "nivel_acceso": "Restringido",
    }
    
    logs_list = []

    try:
        conn = bd.conexion_db()

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:

            #primera consulta: verificamos la ulitma sincronizacion de la base de datos
            sql_sincronizacion = "SELECT MAX(fecha_hora) AS ultima FROM historial_movimientos;"
            cursor.execute(sql_sincronizacion)
            sincronizacion = cursor.fetchone()
            if sincronizacion and sincronizacion["ultima"]:
                auditoria_data["ultima_sincronizacion"] = sincronizacion["ultima"].strftime("%Y-%m-%d %H:%M:%S")
            
            #segunda consulta: recuento de registros alterados
            sql_alterados = "SELECT COUNT(*) AS total FROM historial_movimientos WHERE DATE(fecha_hora) = CURDATE();"
            cursor.execute(sql_alterados)
            alterados = cursor.fetchone()
            if alterados:
                auditoria_data["registros_alterados"] = alterados["total"]

            # de momento dejamos estos datos pero luego se cambiaran
            auditoria_data["token_sesion"] = "abc123xyz"  
            auditoria_data["nivel_acceso"] = "nivel 1 y nivel 2" 
            
            #tercera consulta: obtenemos los datos de quien realizo los movimientos de inventario
            sql_logs = """
                SELECT 
                    CONCAT(u.pri_nom, ' ', u.pri_ape) AS usuario,
                    h.tipo_movimiento AS accion,
                    h.fecha_hora AS fecha
                    FROM historial_movimientos h
                    JOIN usuarios u ON h.id_usuario = u.id_usuario
                    ORDER BY h.fecha_hora DESC
                    LIMIT 10;
            """
            cursor.execute(sql_logs)
            logs_list = cursor.fetchall()

            for log in logs_list:
                if log["fecha"]:
                    log["fecha"] = log["fecha"].strftime("%Y-%m-%d %H:%M:%S")

        return auditoria_data, logs_list
    except Exception as e:
        print(f"Error al obtener conexión: {e}")
    finally:
        if conn:
            conn.close()

def consultas_globales_analisis():
    #vamos a hacer las ultimas consultas para la plantilla de inicio
    try:
        conn = bd.conexion_db()

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            #primera consulta el producto con mayor alza y ademas del calculo porcentual del mismo
            sql_estimado = """
                SELECT
                    m.nombre,
                    p.cantidad_predicha,
                    IFNULL(SUM(CASE WHEN h.tipo_movimiento = 'Salida' THEN h.cantidad END), 0) AS despecho_del_mes_pasado, 
                    ROUND(
                        IF(
                            IFNULL(SUM(CASE WHEN h.tipo_movimiento = 'Salida' THEN h.cantidad END), 0) > 0,
                            ((p.cantidad_predicha - SUM(CASE WHEN h.tipo_movimiento = 'Salida' THEN h.cantidad END)) / SUM(CASE WHEN h.tipo_movimiento = 'Salida' THEN h.cantidad END)) * 100, 0
                        ), 1
                    ) AS incremento_porcentual
                FROM predicciones_demanda p
                INNER JOIN medicamentos m ON p.id_medicamento = m.id_medicamento
                LEFT JOIN lote_inventario l ON m.id_medicamento = l.id_medicamento
                LEFT JOIN historial_movimientos h ON l.id_lote = h.id_lote AND h.fecha_hora >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY p.id_prediccion, m.nombre, p.cantidad_predicha
                ORDER BY incremento_porcentual DESC
                LIMIT 1;
            """
            cursor.execute(sql_estimado)
            resultado_estimado = cursor.fetchone()

            if resultado_estimado:
                producto_lider = resultado_estimado["nombre"]
                # Si el incremento dio negativo (porque la IA predice menos consumo), 
                # mostramos un valor absoluto o un porcentaje base de alza
                incremento = max(resultado_estimado["incremento_porcentual"], 5.0) 
            else:
                producto_lider = "Ninguno"
                incremento = "0.0"

            #segunda consulta productos con bajo umbral
            sql_umbral = """
                SELECT COUNT(DISTINCT id_medicamento) AS bajo_umbral
                FROM lote_inventario
                WHERE stock_actual < 15 AND stock_actual > 0;
            """
            cursor.execute(sql_umbral)
            umbral  = cursor.fetchone()["bajo_umbral"]

            #como tercera he ultima consulta para el analisis tenemos alertas de stock
            sql_alertas  = """
                SELECT 
                    m.nombre,
                    IFNULL(SUM(l.stock_actual), 0) AS stock,
                    ROUND(
                        IF(IFNULL(p.cantidad_predicha, 0) > 0, 
                           (IFNULL(SUM(l.stock_actual), 0) / p.cantidad_predicha) * 30, 
                           90)
                    ) AS dias_cobertura,
                    CASE 
                        WHEN p.probabilidad_alerta IS NOT NULL THEN p.probabilidad_alerta
                        WHEN IFNULL(SUM(l.stock_actual), 0) < 10 THEN 'ALTA'
                        ELSE 'MEDIA'
                    END AS nivel_prioridad
                FROM medicamentos m
                INNER JOIN lote_inventario l ON m.id_medicamento = l.id_medicamento
                LEFT JOIN predicciones_demanda p ON m.id_medicamento = p.id_medicamento
                GROUP BY m.id_medicamento, m.nombre, p.probabilidad_alerta, p.cantidad_predicha
                HAVING stock < 50  -- Mostramos solo los que están bajando stock
                ORDER BY stock ASC
                LIMIT 10;
            """
            cursor.execute(sql_alertas)
            alertas_stock = cursor.fetchall()

            analisis_data = {
            "producto_lider": producto_lider,
            "incremento_estado": incremento,  
            "modelo_ia": "Random Forest Regressor + PMML", 
            "productos_bajo_umbral": umbral
        }

        return analisis_data, alertas_stock

    except Exception as e:
        print(f"❌ Error en consultas_globales_analisis: {e}")
        return {"producto_lider": "N/A", "incremento_estado": "0", "modelo_ia": "Algoritmo Base", "productos_bajo_umbral": 0}, []
    finally:
        if conn:
            conn.close()
