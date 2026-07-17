from database import conexion as bd
import pymysql

#de aqui obtenes los datos para el inventario y lo que se necesite
def obtener_inventario():
    try:
        conn = bd.conexion_db()

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            #obtenemos los datos que solicita el inventario
            sql_inventario = """
                SELECT
                    m.nombre,
                    l.numero_lote AS lote,
                    IFNULL(m.categoria, 'General') AS categoria,
                    IFNULL(l.stock_actual, 0) AS stock,
                    CONCAT((m.id_medicamento % 5) + 1, '-A') AS estante,
                    CASE
                        WHEN l.stock_actual = 0 THEN 'danger'
                        WHEN l.stock_actual < 15 THEN 'warning'
                        ELSE 'success'
                    END AS alerta,
                    CASE
                        WHEN l.stock_actual = 0 THEN 'agotado'
                        WHEN l.stock_actual < 15 THEN 'stock critico'
                        ELSE 'optimo'
                    END AS texto_alerta
                FROM lote_inventario l
                INNER JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
                ORDER BY l.stock_actual ASC;
            """
            cursor.execute(sql_inventario)
            inventario = cursor.fetchall()

        return inventario
    except Exception as e:
        print(f"❌ Error en consultas_inventario: {e}")
    finally:
        if conn:
            conn.close()

#ya de aqui lo usamos lo de la entrada y la salida del inventario
def entrada_inventario(nom, cate, can, lote, fecha_ven, usuario):
    try:
        conn = bd.conexion_db()

        with conn.cursor() as cursor:
            #obtengo el id del usuario para usarlo luego
            sql_usuario = "SELECT id_usuario FROM usuarios WHERE usuario = %s"
            datos_0 = (usuario, )
            cursor.execute(sql_usuario, datos_0)
            id_usuario = cursor.fetchone()[0]

            #buscamos el nombre y la categoria para ignorar la insercion
            sql_insertar = "INSERT IGNORE INTO medicamentos (nombre, categoria) VALUES (%s, %s);"
            datos_1 = (nom, cate)
            cursor.execute(sql_insertar, datos_1)

            #si el medicamento ya existia, actualizamos su categoria de todas formas
            sql_actualizar_cat = "UPDATE medicamentos SET categoria = %s WHERE nombre = %s"
            cursor.execute(sql_actualizar_cat, (cate, nom))

            #buscamos el id del lote
            sql_med = "SELECT id_medicamento FROM medicamentos WHERE nombre = %s"
            datos_2 = (nom, )
            cursor.execute(sql_med, datos_2)
            id_med = cursor.fetchone()[0]

            #ahora actualizamos el lote
            sql_actualizar = """
                INSERT INTO lote_inventario (id_medicamento, numero_lote, stock_actual, fecha_vencimiento)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE stock_actual = stock_actual + %s
            """
            datos_3 = (id_med, lote, can, fecha_ven, can)
            cursor.execute(sql_actualizar, datos_3)

            #ahora buscamos el id del lote para el historial
            sql_lote = "SELECT id_lote FROM lote_inventario WHERE id_medicamento = %s AND numero_lote = %s"
            datos_4 = (id_med, lote)
            cursor.execute(sql_lote, datos_4)
            id_lote = cursor.fetchone()[0]

            #ahora lo resgistramos en el historial
            sql_historial = """
                INSERT INTO historial_movimientos (id_lote, id_usuario, tipo_movimiento, cantidad)
                VALUES (%s, %s, 'Entrada', %s)
            """
            datos_5 = (id_lote, id_usuario, can)
            cursor.execute(sql_historial, datos_5)
            conn.commit()
    except Exception as e:
        print(f"❌ Error en consultas_inventario: {e}")
    finally:
        if conn:
            conn.close()

def salida_inventario(id_medicamento, cantidad, motivo, usuario):
    try:
        conn = bd.conexion_db()

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            #obtengo el id del usuario para usarlo luego
            sql_usuario = "SELECT id_usuario FROM usuarios WHERE usuario = %s"
            datos_0 = (usuario, )
            cursor.execute(sql_usuario, datos_0)
            id_usuario = cursor.fetchone()["id_usuario"]

            #buscamos si tenemos el id del lote y si tiene stock
            sql_stock = "SELECT id_lote, stock_actual FROM lote_inventario WHERE numero_lote = %s"
            datos_1 = (id_medicamento, )
            cursor.execute(sql_stock, datos_1)
            lote = cursor.fetchone()

            if not lote or lote["stock_actual"] < cantidad:
                return {"error": "Lote no encontrado o stock insuficiente"}
            
            id_lote = lote["id_lote"]

            #actualimos el stock del lote
            sql_salida = "UPDATE lote_inventario SET stock_actual = stock_actual - %s WHERE id_lote = %s"
            datos_2 = (cantidad, id_lote)
            cursor.execute(sql_salida, datos_2)

            #ahora actualizamos el historial
            sql_historial = """
                INSERT INTO historial_movimientos (id_lote, id_usuario, tipo_movimiento, cantidad)
                VALUES (%s, %s, 'Salida', %s)
            """
            datos_3 = (id_lote, id_usuario, cantidad)
            cursor.execute(sql_historial, datos_3)

            conn.commit()
    except Exception as e:
        print(f"❌ Error en consultas_inventario: {e}")
    finally:
        if conn:
            conn.close()

def obtener_medicamentos_para_select():
    """Obtiene la lista de medicamentos con stock disponible para el select de salida."""
    try:
        conn = bd.conexion_db()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT l.numero_lote, m.nombre, l.stock_actual
                FROM lote_inventario l
                INNER JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
                WHERE l.stock_actual > 0
                ORDER BY m.nombre ASC
            """
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener medicamentos: {e}")
        return []
    finally:
        if conn:
            conn.close()
