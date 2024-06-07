import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def send_email(email, nombre, fecha, hora, barber):
    #credenciales
    user = st.secrets["emails"]["smtp_user"]
    password = st.secrets["emails"]["smtp_password"]
    email_sender = "Latorre Estudio"
    
    #configuracion del servidor
    msg = MIMEMultipart()
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    #Parametros de mail
    msg['From'] = email_sender
    msg['To'] = email
    msg['Subject'] = "Reservaste un turno en Latorre Estudio"
    
    #Mensaje de mail
    message = f'''
    <html>
    <body>
    <p>Hola {nombre},</p>
    <p>Tu turno fue reservado!</p>
    <p>Te esperamos el {fecha}, a las {hora}hs.</p>
    <p>Elegiste a {barber} como tu peluquero.</p>
    <p>Gracias por elegir Latorre Estudio.</p>
    <img src="cid:logo">
    </body>
    </html>
    '''
    
    msg.attach(MIMEText(message, 'html'))
    
    with open("assets/latoLogo.png", "rb") as logo:
        logo_mime = MIMEImage(logo.read())
        logo_mime.add_header("Content-ID", "<logo>")
        msg.attach(logo_mime)
    
    #Conexion al servidor
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(user, password)
        server.sendmail(email_sender, email, msg.as_string())
        server.quit()
        
    except smtplib.SMTPException:
        st.exception("Error al enviar el email") 





