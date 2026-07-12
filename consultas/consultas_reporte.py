from database import conexion as bd
import pymysql

def consulta_reporte(inicio, fin):
    try:
        conn = bd.conexion_db()

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            #hacemos la consula de los balances
            sql_despachos = """
                SELECT 
                    IFNULL(SUM(h.cantidad), 0) AS total,
                    IFNULL(AVG(p.cantidad_predicha)) AS tendencia
                FROM historial_movimientos h
                INNER JOIN predicciones_demanda p ON l.id_medicamento = p.id_medicamento
                WHERE tipo_movimiento = 'Salida'
                    AND DATE(fecha_hora) BETWEEN %s AND %s;
            """
            datos = (inicio, fin)

            cursor.execute(sql_despachos, datos)
            despachos = cursor.fetchall()

            despacho_total = despachos["total"]
            ia = despachos["tendencia"]

            #calculamos con la tendencia
            if despacho_total > ia and ia > 0:
                tendencia = "Demanda supera de la IA"
            elif despacho_total < ia and ia > 0:
                tendencia = "Poca demanda de la IA"
            else:
                tendencia = "Todo en orden por parte de la IA"
            
            #ahora calculamos las bajas
            sql_bajas = """
            SELECT IFNULL(COUNT(id_lote), 0) AS total_bajas
            FROM lote_inventario
            WHERE fecha_vencimiento <= CURDATE();
            """
            cursor.execute(sql_bajas)
            bajas = cursor.fetchone()["total_bajas"]

            #hacemos entonces tambien las alertas criticas
            sql_alertas = """
            SELECT IFNULL(COUNT(id_lote), 0) AS total_alertas
            FROM lote_inventario
            WHERE fecha_vencimiento BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
                AND stock_actual > 0;
            """
            cursor.execute(sql_alertas)
            alertas = cursor.fetchone()["total_alertas"]

            #luego para terminar hacemos la consulta de los movimientos 
            sql_movimientos = """
                SELECT
                    DATE_FORMAT(h.fecha_hora, '%%d/%%m/%%Y %%h:%%i %%p') AS fecha,
                    u.usuario,
                    h.tipo_movimiento AS accion,
                    h.tipo_movimiento AS accion_tipo,
                    m.nombre AS medicamento,
                    l.numero_lote AS lote,
                    'Movimiento del inventario' as motivo
                FROM historial_movimientos h
                INNER JOIN lote_inventario l ON h.id_lote = l.id_lote
                INNER JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
                INNER JOIN usuarios u ON h.id_usuario = u.id_usuario
                WHERE DATE(h.fecha_hora) BETWEEN %s AND %s
                PRDER BY h.fecha_hora DESC;
            """
            cursor.execute(sql_movimientos, datos)
            movimientos = cursor.fetchall()


            reportes = {
                "despachos_total": despacho_total,
                "despachos_tendencia": tendencia,
                "bajas_total": bajas,
                "lotes_vencer": alertas,
                "movimientos": movimientos
            }
        return reportes
    except Exception as e:
        print(f"❌ Error en consultas_reportes: {e}")
    finally:
        if conn:
            conn.close()


