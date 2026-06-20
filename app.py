from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app =  FastAPI
plantillas = Jinja2Templates(directory="Templates")

#definos la ruta principal y la usamos de espejo para la del login
#ahora definimos mediante una funcion la logica y el rederizado de la una plantilla
@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return plantillas.TemplateResponse("Inicio_Sesion/inicio_sesion.html", {request: Request})

@app.get("/registro", response_class=HTMLResponse)
async def register(request: Request):
    return plantillas.TemplateResponse("Inicio_Sesion/registro.html", {request: Request})

@app.get("/Inventario", response_class=HTMLResponse)
async def ver_inventario(request: Request):
    return plantillas.TemplateResponse("Inventario/inventario.html", {"request": request})

@app.get("/inventario/entrada", response_class=HTMLResponse)
async def formulario_entrada(request: Request):
    return plantillas.TemplateResponse("Inventario/entrada.html", {"request": request})


@app.get("/inventario/salida", response_class=HTMLResponse)
async def formulario_salida(request: Request):
    return plantillas.TemplateResponse("Inventario/salida.html", {"request": request})