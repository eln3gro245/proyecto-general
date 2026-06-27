from database import conexion as con
import guardia_de_seguridad as seg

def login(user, password):
    pass

def validar_registro(username):
    conn = con.conexion_db()
    cursor = conn.cursor()

    try:
        #lo paso todo a texto para evitar que el usuario pueda acceder a la consulta directamete
        consulta = "SELECT * FROM farma_norte.usuarios where usuario = %s"
        datos = (username,)
        #de esta manera logramos que convertir a texto lo que el usuario pongo no dandole libertad dentro de la consulta
        cursor.execute(consulta, datos)
        validacion = cursor.fetchone

        conn.commit()

        return validacion
    except Exception as error:
        print(f"error al insertar: {error}")
    finally:
        cursor.close()
        conn.close() 

def registrar(name, name2, lastname, lastname2, username, password):
    conn = con.conexion_db()
    cursor = conn.cursor()

    try:
        contraseña_hasheada = seg.hashear_contrasena(password)
        consulta = """INSERT INTO usuarios(pri_nom, seg_nom, pri_ape, seg_ape, usuario, contrasena)
                      VALUES(%s,%s,%s,%s,%s,%s)"""
        datos = (name, name2, lastname, lastname2, username, contraseña_hasheada)
        cursor.execute(consulta, datos)

        conn.commit()

        return True
    except Exception as error:
        print(f"error al insertar: {error}")
        return False
    finally:
        cursor.close()
        conn.close() 