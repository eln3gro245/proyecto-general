from database import conexion as con
import seguridad.guardia_de_seguridad as seg

#y aqui vemos si sus credenciales son correctas
def login(user, password):
    conn = con.conexion_db()
    cursor = conn.cursor()

    try:
        #lo paso todo a texto para evitar que el usuario pueda acceder a la consulta directamete
        consulta = "SELECT contrasena, id_rol FROM farma_norte.usuarios where usuario = %s"
        datos = (user,)
        #de esta manera logramos que convertir a texto lo que el usuario pongo no dandole libertad dentro de la consulta
        cursor.execute(consulta, datos)
        resultado = cursor.fetchone()

        if resultado is None:
            return False

        contrasena_hasheada = resultado[0]
        id_rol = resultado[1]

        if seg.verificar_contrasena(password, contrasena_hasheada):
            return id_rol
        else:
            return False
    except Exception as error:
        print(f"error al logearse: {error}")
        return False
    finally:
        cursor.close()
        conn.close()

#primero antes que nada validamos si el usuario no esta en la base de datos
def validar_registro(username):
    conn = con.conexion_db()
    cursor = conn.cursor()

    try:
        consulta = "SELECT * FROM farma_norte.usuarios where usuario = %s"
        datos = (username,)
        cursor.execute(consulta, datos)
        validacion = cursor.fetchone()

        return validacion
    except Exception as error:
        print(f"error al validar registro: {error}")
    finally:
        cursor.close()
        conn.close() 
#para luego agregarlo a la misma
def registrar(name, name2, lastname, lastname2, username, password):
    conn = con.conexion_db()
    cursor = conn.cursor()

    try:
        contrasena_hasheada = seg.hashear_contrasena(password)
        consulta = """INSERT INTO usuarios(pri_nom, seg_nom, pri_ape, seg_ape, usuario, contrasena, id_rol)
                      VALUES(%s,%s,%s,%s,%s,%s,3)"""
        datos = (name, name2, lastname, lastname2, username, contrasena_hasheada)
        cursor.execute(consulta, datos)

        conn.commit()

        return True
    except Exception as error:
        print(f"error al insertar: {error}")
        return False
    finally:
        cursor.close()
        conn.close() 