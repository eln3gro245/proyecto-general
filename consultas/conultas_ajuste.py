from database import conexion as bd
import pymysql

#aqui tenemos las distintas cosultas para la ruta de ajuste para cada caso requerido
def consultas_ajuste_frecuencia():
    try:
        conn = bd.conexion_db()

        with conn.cursor() as cursor:
            sql_fecha = "SELECT creado_el FROM predicciones_demanda ORDER BY id_prediccion DESC LIMIT 1;"
            cursor.execute(sql_fecha)
            resultado = cursor.fetchone()

        return resultado
    except Exception as e:
        print(f"Error al ejecutar consultas globales: {e}")
    finally:
        if conn:
            conn.close()

def consulta_ajuste_criticos(margen: int):
    try:
        conn = bd.conexion_db()

        with conn.cursor() as cursor:
            sql_critico = """
                SELECT l.numero_lote, m.nombre, l.stock_actual, l.fecha_vencimiento,
                    DATADIFF(l.fecha_vencimiento, CURDATE()) AS dias_restantes
                FROM lote_inventario l
                INNER JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
                WHERE DATADIFF(l.fecha_vencimiento, CURDATE()) <= %s
                    AND DATADIFF(l.fecha_vencimiento, CURDATE()) > 0
                    AND l.stock_actual > 0
            """
            datos = (margen,)

            cursor.execute(sql_critico, datos)
            resultado = cursor.fetchall()

        return resultado
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
    finally:
        if conn:
            conn.close()

def obtener_ajuste_farmacia(nombre, codigo, ubi):
    try:
        conn = bd.conexion_db()

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql_farmacia = "SELECT nombre_farmacia, codigo_sucursal, ubicacion FROM datos_farmacia;"
            cursor.execute(sql_farmacia)
            resultado = cursor.fetchone()
        
        return resultado
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return False
    finally:
        if conn:
            conn.close()

#ya apartir de aqui la funciones modifican el html
def modificar_ajuste_farmacia(nombre: str, codigo: str, ubi: str):
    try:
        conn = bd.conexion_db()
        with conn.cursor() as cursor:
            sql_farmacia = """
                UPDATE datos_farmacia 
                SET nombre_farmacia = %s, codigo_sucursal = %s, ubicacion = %s 
                WHERE id = 1;
            """
            valores = (nombre, codigo, ubi)
            cursor.execute(sql_farmacia, valores)
            conn.commit() 
        return True
    except Exception as e:
        print(f"Error al actualizar los datos: {e}")
        return False
    finally:
        if conn:
            conn.close()

#esta funcion solo la ejecuta el super admin
def cambio_rol(id: int, usuario_id: int):
    try:
        conn = bd.conexion_db()

        with conn.cursor() as cursor:

            sql_rol = "UPDATE usuarios SET id_rol = %s WHERE id_usuario = %s"
            datos = (id, usuario_id)
            cursor.execute(sql_rol, datos)

            conn.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar los datos: {e}")
        return False
    finally:
        if conn:
            conn.close()