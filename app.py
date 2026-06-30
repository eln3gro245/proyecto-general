from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Query
from fastapi import Form
import login as log

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="farma_norte_secret_key_123")
plantillas = Jinja2Templates(directory="templates")


#========================== INICIO DE SESION =============================

#definos la ruta principal y la usamos de espejo para la del login
#ahora definimos mediante una funcion la logica y el rederizado de la una plantilla
#el metodo get es para mostrar la platilla
@app.get("/", response_class=HTMLResponse)
async def mostrar_login_normal(request: Request): # por lo que este solo  la rederiza 
    return plantillas.TemplateResponse("Inicio_Sesion/inicio_sesion.html", {"request": request})

#por debido a eso hacemos una nueva funcion que se encargara de recibir la informacion del formulario del HTML
@app.post("/", response_class=HTMLResponse)
async def procesar_login(request: Request, username: str = Form(...), password: str  = Form(...)):
    rol = log.login(username, password)
    if rol:
        request.session['usuario'] = username
        request.session['rol'] = rol

        #nos redirigimos a la siguiente platanlla limpiando el servidor de las peticiones http de formulario
        return RedirectResponse(url="/Inicio", status_code=303) #este codigo es el encargado de eso le dice al servido llevame a este url y limpia lo que esta atras
    else:
        return plantillas.TemplateResponse("Inicio_Sesion/inicio_sesion.html", {
                "request": request,
                "mensaje": "Error credenciales incorrectas"
            })


#========================== REGISTRAR =============================

# igual manera solo para mostrar
@app.get("/registro", response_class=HTMLResponse)
async def mostrar_registrador(request: Request):
    return plantillas.TemplateResponse("Inicio_Sesion/registro.html", {"request": request})

#y aqui para recibir informacion
@app.post("/registro", response_class=HTMLResponse)
async def procesar_registrardor(request: Request,
                                name: str = Form(...),
                                name2: str = Form(None),
                                lastname: str = Form(...),
                                lastname2: str = Form(None),
                                username: str = Form(...),
                                password: str = Form(...)):
    
    validar = log.validar_registro(username)
    if validar is None:
        #si no hay ningun usuario con el mismo nombre lo registramo
        exito = log.registrar(name, name2, lastname, lastname2, username, password)
        if exito:
            #por si todo sale bien
            return plantillas.TemplateResponse("Inicio_Sesion/inicio_sesion.html", {
                "request": request,
                "mensaje": "¡Registro exitoso! Inicia sesión."
            })
        else:
            #en caso de que ocurra un error 
            return plantillas.TemplateResponse("Inicio_Sesion/registro.html", {
                "request": request,
                "error": "Error interno al guardar los datos. Intente más tarde."
            })
    else:
        #si ahi una coincidencia le decimos al usuario
        return plantillas.TemplateResponse("Inicio_Sesion/registro.html", {
            "request": request,
            "error": "Lo siento, este nombre de usuario ya está en uso. Intenta con otro."
        })

#========================== DASHBOARD =============================

@app.get("/Inicio", response_class=HTMLResponse)
async def inicio_principal(request: Request, tab: str = Query("principal")):
    tab_actual = tab

    if tab_actual not in ["principal", "analisis", "auditoria"]:
        tab_actual = "principal"

    rol_usuario = request.session.get('rol', 3)

    plantillas.env.globals["Activar_tab"] = tab_actual
    plantillas.env.globals["user_role"] = rol_usuario
    
    return plantillas.TemplateResponse("Inicio/inicio.html", {"request": request})

#========================== INVENTARIO =============================

@app.get("/Inventario", response_class=HTMLResponse)
async def ver_inventario(request: Request):
    return plantillas.TemplateResponse("Inventario/inventario.html", {"request": request})

@app.get("/Inventario/Entrada", response_class=HTMLResponse)
async def formulario_entrada(request: Request):
    return plantillas.TemplateResponse("Inventario/entrada.html", {"request": request})

@app.get("/Inventario/Salida", response_class=HTMLResponse)
async def formulario_salida(request: Request):
    return plantillas.TemplateResponse("Inventario/salida.html", {"request": request})

#========================== AJUSTES =============================

@app.get("/Ajuste", response_class=HTMLResponse)
async def hacer_ajuste(request: Request):
    return plantillas.TemplateResponse("Ajuste/ajuste.html", {"request": request})

#========================== REPORTES =============================

@app.get("/Reportes", response_class=HTMLResponse)
async def generacion_de_reportes(request: Request):
    return plantillas.TemplateResponse("Ajuste/ajuste.html", {"request": request})