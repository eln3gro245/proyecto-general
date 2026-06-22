import pymysql

def conexion_db():
    conexion = pymysql.connect(
        host= "localhost",
        user= "root", 
        password= "admin",
        database= "farma_norte"
    )
    return conexion