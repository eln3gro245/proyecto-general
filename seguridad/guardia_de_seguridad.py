from passlib.context import CryptContext

#aqui le decimos el algoritmo con el que queremos que hashee la contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashear_contrasena(contrasena: str):
    #y aqui es donde se hashea usando la variable de configuracion
    return pwd_context.hash(contrasena)

def verificar_contrasena(contrasena_normal: str, contrasena_hasheada: str):
    #y aqui lo que hacemos es comparar la contraseña que viene del formulario con la hasheada
    return pwd_context.verify(contrasena_normal, contrasena_hasheada)