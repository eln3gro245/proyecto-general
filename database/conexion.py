import pymysql

def conexion_db():
    conexion = pymysql.connect(
        host= "localhost",
        port= 3306,
        user= "root", 
        password= "root",
        database= "farma_norte"
        )
    return conexion