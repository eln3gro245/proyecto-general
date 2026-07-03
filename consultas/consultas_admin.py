from database import conexion as db
import pymysql

def consultas_admin(usuario_activo: str):
    data_admin = {
        "nombre_usuario": usuario_activo,
        "total_productos": 0,
        "ventas_dia": 0,
        "alertas_criticas": 0,
    }

    try:
        conn = db.conexion_db()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            #total de medicamentos en la base de datos
            cursor.execute("SELECT COUNT(*) AS total FROM medicamentos")
            result = cursor.fetchone()
            if result:
                data_admin["total_productos"] = result["total"]
        
            #total de ventas del dia
            sql_ventas = """
                SELECT COUNT(*) AS total 
                FROM historia_movimientos 
                WHERE tipo_movimiento = 'Salida' AND DATE(fecha_movimiento) = CURDATE()
            """
            cursor.execute(sql_ventas)
            ventas = cursor.fetchone()
            if ventas:
                data_admin["ventas_dia"] = ventas["total"]
            
            #alertas criticas
            sql_alertas = """
                SELECT COUNT(*) AS total
                FROM (
                    SELECT id_medicamento, SUM(stock_actual) AS total_stock
                    FROM lote_inventario
                    GROUP BY id_medicamento
                    HAVING stock_actual <= 10
                ) AS subconsulta
            """
            cursor.execute(sql_alertas)
            alertas = cursor.fetchone()
            if alertas:
                data_admin["alertas_criticas"] = alertas["total"]
        
        return data_admin
    except Exception as e:
        print(f"Error al realizar consultas: {e}")
    finally:
        if conn:
            conn.close()
    