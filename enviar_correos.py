from prediccion_IA import obtener_predicciones as pred
from jinja2 import Environment, FileSystemLoader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib
import json
import os

load_dotenv()
env_jinja = Environment(loader=FileSystemLoader("templates"))

#cargamos el json del modulo principal donde esta el correo
def carga_json():
    try:
        with open("config_sistema.json", "r") as f:
            confi = json.load(f)
            return confi.get("correo", "josehdezbracho@gmail.com")
    except FileNotFoundError:
        return "josehdezbracho@gmail.com"

#y aqui es donde enviaremos los correos
def enviar_correo():
    lista = pred.obtener_predicciones()

    if not lista:
        print("⚠️ No hay predicciones hoy para enviar por correo.")
        return
    
    #cargamos el correo en el json
    correo = carga_json()

    #ajustamos los detalles para el envio del correo
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📦 Pedido Automático Farma Norte"
    msg["From"] = smtp_user
    msg["To"] = correo

    try:
        #buscamos el html para el estilo del correo
        plantilla = env_jinja.get_template("Componentes\correos.html")
        html_renderizado = plantilla.render(producto=lista)
        msg.attach(MIMEText(html_renderizado, "html", "utf-8"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(smtp_user, correo, msg.as_string())
    except Exception as e:
            print(f"❌ Error al procesar o enviar el correo: {e}")