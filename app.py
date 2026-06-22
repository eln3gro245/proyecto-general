from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app =  FastAPI
plantillas = Jinja2Templates(directory="Templates")

#definos la ruta principal y la usamos de espejo para la del login
#ahora definimos mediante una funcion la logica y el rederizado de la una plantilla
@app.get("/", response_class=HTMLResponse)
@app.get("/Login", response_class=HTMLResponse)
async def login(request: Request,
                username: str = Form(...),
                password: str = Form(...)):
    
    return plantillas.TemplateResponse("Inicio_Sesion/inicio_sesion.html", {request: Request})

@app.get("/Registro", response_class=HTMLResponse)
async def register(request: Request,
                   fullname: str = Form(...),
                   username: str = Form(...),
                   password: str = Form(...)):
    return plantillas.TemplateResponse("Inicio_Sesion/registro.html", {request: Request})

@app.get("/Inicio", response_class=HTMLResponse)
async def inicio_principal(request: Request, tab: str = Query("principal")):
    tab_actual = tab

    if tab_actual not in ["principal", "analisis", "auditoria"]:
        tab_actual = "principal"
    
    return plantillas.TemplateResponse("Inicio/incio.html", {"request": request, "Activar_tab": tab_actual})

@app.get("/Inventario", response_class=HTMLResponse)
async def ver_inventario(request: Request):
    return plantillas.TemplateResponse("Inventario/inventario.html", {"request": request})

@app.get("/Inventario/Entrada", response_class=HTMLResponse)
async def formulario_entrada(request: Request):
    return plantillas.TemplateResponse("Inventario/entrada.html", {"request": request})


@app.get("/Inventario/Salida", response_class=HTMLResponse)
async def formulario_salida(request: Request):
    return plantillas.TemplateResponse("Inventario/salida.html", {"request": request})

@app.get("/Ajuste", response_class=HTMLResponse)
async def hacer_ajuste(request: Request):
    return plantillas.TemplateResponse("Ajuste/ajuste.html", {request: Request})

@app.get("/Reportes", response_class=HTMLResponse)
async def generacion_de_reportes(request: Request):
    return plantillas.TemplateResponse("Ajuste/ajuste.html", {request: Request})