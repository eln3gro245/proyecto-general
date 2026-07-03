from fastapi import HTTPException, status, Request

#verificamos la sesion
def verificar_entrada(request: Request):
    #si no esta logeado lo sacamos
    rol = request.session.get('rol')
    if not rol:
        raise HTTPException(
            status_code=303,
            headers={"Location": "/" }
        )
    return rol
    
#verificamos el roles
def verificar_rol_administrativo(request: Request):
    #reutilizamos la funcion anterior
    rol = verificar_entrada(request)

    if rol not in [1,2]:
         raise HTTPException(
            status_code=303,
            headers={"Location": "/" }
        )
    return rol

def Verificamos_al_papa_de_los_helados(request: Request):
    #reutilizamos la funcion anterior
    rol = verificar_entrada(request)

    if rol != 1:
         raise HTTPException(
            status_code=303,
            headers={"Location": "/" }
        )
    return rol