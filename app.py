from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import seguridad.verificar_sesiones_roles as seguridad
from consultas import consultas_reporte as reporte
from consultas import consultas_inventario as ver
from consultas import conultas_ajuste as ajuste
from consultas import consultas_admin as admin
from fastapi.templating import Jinja2Templates
import consultas.consultas_inicio as consulta
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Query
from prediccion_IA import predicciones as p
from datetime import datetime, timedelta
from fastapi import Form, Depends
import enviar_correos as correo
from dotenv import load_dotenv
import login as log
import json
import os

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRECT_KEY"))
plantillas = Jinja2Templates(directory="templates")

#========================== PETICIONES REPETITIVAS(CONTEXTO GLOBAL) =============================
#hacemos es que para que cada vez que necesitemos algo siempre vamos ultilizar para realizar la peticiones al jinja 
#le agregamos un contexto global que siempre lo tengamos a mano 
def contexto(request: Request):
    return {
        "user_role": request.session.get('rol', 3),       
        "usuario_actual": request.session.get('usuario') #nota es mejor hacerlo para cada cosa repetitiva de manera separada tanto la funcion como agregarla context
    }

plantillas.context_processors.append(contexto)

#========================== PREDICCIONES DE IA =============================
#aqui lo que hacemos es que cuando iniciamos el servidor cargamos las prediccones dentro de la base de datos
@app.on_event("startup")
async def cargar_prediccoines_IA():
    try:
        try:
            with open("config_sistema.json", "r") as f:
                confi = json.load(f)
                frecuencia = confi.get("frecuencia_analisis", "Semanal")
                margen = confi.get("margen_vencimiento", 30)
        except FileNotFoundError:
            frecuencia = "Semanal" #dejamos este dato por si ocurre un error al abrir el json
            margen = 30

        fecha_hoy = datetime.now()
        semana = fecha_hoy.weekday()

        ultima_ejecucion = ajuste.consultas_ajuste_frecuencia()

        ya_ejecuto_semana = False
        ya_ejecuto_hoy = False

        if ultima_ejecucion:
            semana_actual = fecha_hoy.isocalendar()[1]
            ano_actual = fecha_hoy.year

            ejecucion = ultima_ejecucion[0]

            semana_ultima = ejecucion.isocalendar()[1]
            ano_ultimo = ejecucion.year

            if semana_ultima == semana_actual and ano_ultimo == ano_actual:
                ya_ejecuto_semana = True
            if ejecucion.date() == fecha_hoy.date():
                ya_ejecuto_hoy = True
        
        #ademas configuramos con los ajuste para activar las predicciones de la IA 
        if frecuencia == "Inmediato":
            p.generar_y_guerdar_predicciones_semanales()
            correo.enviar_correo()
        elif frecuencia == "Diario" and not ya_ejecuto_hoy:
            p.generar_y_guerdar_predicciones_semanales()
            correo.enviar_correo()
        elif frecuencia == "Semanal" and semana == 0 and not ya_ejecuto_semana:
            p.generar_y_guerdar_predicciones_semanales()
            correo.enviar_correo()
        
        lotes_riesgo = ajuste.consulta_ajuste_criticos(margen)
        if lotes_riesgo:
            pass

    except Exception as e:
        print(f"Error al obtener los datos: {e}")

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

@app.get("/Inicio", response_class=HTMLResponse, dependencies=[Depends(seguridad.verificar_entrada)])
async def principal(request: Request, tab: str = Query("principal")):
    tab_actual = tab
    #========================== SELECTOR DE PLANTILLA =============================

    if tab_actual not in ["principal", "analisis", "auditoria"]:
        tab_actual = "principal"

    #nombre tal cual lo espera el html para cambiar de manera dinamica la plantilla que se esta mostrando en el dashboard
    stats = {}
    auditoria_data = {}
    analisis_data = {}
    alerta = {}
    logs_list = []


    #========================== PRINCIPAL =============================
    #ya con esta funcion realiza la consulta para luego enviarla en la peticion de fastapi
    if tab_actual == "principal":
        stats = consulta.consultas_globales_principal()

    #========================== AUDITORIA =============================
    #de igual forma con esta funcion realiza la consulta para luego enviarla en la peticion de fastapi
    elif tab_actual == "auditoria":
        auditoria_data, logs_list = consulta.consultas_globales_auditoria()

    #========================== ANALISIS =============================
    elif tab_actual == "analisis":
        analisis_data, alerta = consulta.consultas_globales_analisis()

    return plantillas.TemplateResponse("Inicio/inicio.html", {"request": request, 
                                                              "stats": stats, 
                                                              "auditoria_data": auditoria_data, 
                                                              "logs_list": logs_list,
                                                              "analisis_data": analisis_data,
                                                              "alerta": alerta,
                                                              "active_tab": tab_actual})

#========================== INVENTARIO =============================

@app.get("/Inventario", response_class=HTMLResponse, dependencies=[Depends(seguridad.verificar_entrada)])
async def inventario(request: Request):
    inventario = ver.obtener_inventario()
    return plantillas.TemplateResponse("Inventario/inventario.html", {"request": request,
                                                                      "medicamentos": inventario})

@app.get("/inventario/entrada", response_class=HTMLResponse, dependencies=[Depends(seguridad.verificar_rol_administrativo)])
async def get_entrada(request: Request):
    return plantillas.TemplateResponse("Inventario/entrada.html", {"request": request})

@app.post("/inventario/entrada", response_class=HTMLResponse, dependencies=[Depends(seguridad.verificar_rol_administrativo)])
async def formulario_entrada(request: Request,
                             nombre: str = Form(...),
                             categoria: str = Form(...),
                             cantidad: int = Form(...),
                             lote: str = Form(...),
                             proveedor: str = Form(None), #este por ahora no lo vamos a usar por ahora
                             fecha_vencimiento: str = Form(...)):
    try:
        usuario = request.session.get('usuario')
        ver.entrada_inventario(nombre, categoria, cantidad, lote, fecha_vencimiento, usuario)
        return RedirectResponse(url="/Inventario", status_code=303)
    except Exception as e:
        print(f"Error en entrada: {e}")
        return {"error": "No se pudo registrar la entrada"}

@app.get("/inventario/salida", response_class=HTMLResponse, dependencies=[Depends(seguridad.verificar_entrada)])
async def get_salida(request: Request):
    medicamentos = ver.obtener_medicamentos_para_select()
    usuario_actual = request.session.get('usuario')
    return plantillas.TemplateResponse("Inventario/salida.html", {
        "request": request,
        "medicamentos": medicamentos,
        "current_user": usuario_actual
    })

@app.post("/inventario/salida", response_class=HTMLResponse, dependencies=[Depends(seguridad.verificar_entrada)])
async def formulario_salida(request: Request,
                            medicamento_id: str = Form(...),
                            cantidad: int = Form(...),
                            motivo: str = Form(...)):
    try:
        usuario = request.session.get('usuario')
        ver.salida_inventario(medicamento_id, cantidad, motivo, usuario)
        return RedirectResponse(url="/Inventario", status_code=303)
    except Exception as e:
        print(f"Error en salida: {e}")
        return {"error": "No se pudo procesar el despacho"}

#========================== AJUSTES =============================

@app.get("/Ajuste", response_class=HTMLResponse, dependencies=[Depends(seguridad.verificar_entrada)])
async def ajustes(request: Request):
    try:
        with open("config_sistema.json", "r") as f:
            datos = json.load(f)  
    except FileNotFoundError:
        datos = {
            "margen_vencimiento": 30,
            "frecuencia_analisis": "Semanal",
            "server": "localhost"
        }
    farmacia = ajuste.obtener_ajuste_farmacia()
    usuario = {
        "nombre": request.session.get('usuario'),
        "id": request.session.get('rol')
    }

    return plantillas.TemplateResponse("Ajustes/ajustes.html", {"request": request,
                                                              "op": usuario,
                                                              "config": datos,
                                                              "farmacia": farmacia})

#llamamos a la ruta que hace referencia el html para ejecutar la logica
@app.post("/ajustes/guardar-parametros", response_class=HTMLResponse, dependencies=[Depends(seguridad.verificar_entrada)])
def guardar_parametros(request: Request,
                       margen_vencimiento: str = Form(None),
                       frecuencia_analisis: str = Form(None)):
    try:
        #hacemos un diccionario para usarlo luego
        datos = {
            "margen_vencimiento": margen_vencimiento,
            "frecuencia_analisis": frecuencia_analisis,
            "server": "localhost",
            "correo": os.getenv("CORREO")
        }
        with open("config_sistema.json", "r") as f:
            json.dump(datos, f)
        
        return RedirectResponse(url="/Ajuste", status_code=303)
    except Exception as e:
        print(f"Error: {e}")
        return RedirectResponse(url="/Ajuste?error=true", status_code=303)
    
@app.post("/ajustes/actualizar-datos", response_class=HTMLResponse, dependencies=[Depends(seguridad.verificar_entrada)])
def actualizacion_datos(request: Request,
                        nombre_farmacia: str = Form(None),
                        codigo_sucursal: str = Form(None),
                        ubicacion: str = Form(None)):
    try:
        ajuste.modificar_ajuste_farmacia(nombre_farmacia, codigo_sucursal, ubicacion)
        return RedirectResponse(url="/Ajuste", status_code=303)
    except Exception as e:
        print(f"Error: {e}")
        return RedirectResponse(url="/Ajuste?error=true", status_code=303)

@app.post("/ajustes/cambiar-rol", response_class=HTMLResponse, dependencies=[Depends(seguridad.Verificamos_al_papa_de_los_helados)])
def cambio_rol(request: Request,
               usuario_id: int = Form(...),
               nuevo_rol_id: int = Form(...)):
    try:
        ajuste.cambio_rol(nuevo_rol_id, usuario_id)
        return RedirectResponse(url="/Ajuste", status_code=303)
    except Exception as e:
        print(f"Error: {e}")
        return RedirectResponse(url="/Ajuste?error=true", status_code=303)
    

#========================== REPORTES =============================

@app.get("/Reportes", response_class=HTMLResponse, dependencies=[Depends(seguridad.verificar_rol_administrativo)])
async def reportes(request: Request,
                   fecha_inicio: str = Query(None),
                   fecha_fin: str = Query(None)):
    #de normal las fechas estaran en none pero las vamos a calcular ahora por los 30 dias automaticamente
    if not fecha_fin:
        fecha_fin = datetime.now().strftime("%Y-%m-%d")
    if not fecha_inicio:
        fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    datos_reportes = reporte.consulta_reporte(fecha_inicio, fecha_fin)

    return plantillas.TemplateResponse("Reportes/reportes.html", {"request": request,
                                                                  "reportes": datos_reportes,
                                                                  "filtros": {"inicio": fecha_inicio, "fin": fecha_fin},
                                                                  "movimientos_list": datos_reportes["movimientos"]})

#========================== ADMIN =============================

@app.get("/Admin", response_class=HTMLResponse, dependencies=[Depends(seguridad.verificar_rol_administrativo)])
async def ver_admin(request: Request, usuario_activo: str = Depends(seguridad.verificar_entrada)):
    datos_admin = admin.consultas_admin(usuario_activo)
    return plantillas.TemplateResponse("Admin/admin.html", {"request": request,
                                                            "datos_admin": datos_admin["nombre_usuario"],
                                                            "total_productos": datos_admin["total_productos"],
                                                            "ventas_dia": datos_admin["ventas_dia"],
                                                            "alertas_criticas": datos_admin["alertas_criticas"]})

#========================== CERRAR SESION =============================

@app.get("/Logout")
async def logout(request: Request):
    # Limpia por completo la sesión del usuario
    request.session.clear() 
    
    # Redirige a la página de login 
    response = RedirectResponse(url="/", status_code=303)
    
    return response
