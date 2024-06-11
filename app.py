import streamlit as st
from streamlit_option_menu import option_menu
from datetime import date
from send_email import send_email
from google_sheets import GoogleSheets
import re
import uuid
from google_calendar import GoogleCalendar
import numpy as np
import datetime as dt
import pytz

#VARIABLES
page_title = "Latorre Estudio"
page_icon = "assets/latoLogo.png"
layout = "centered"
cortes = [
    "assets/corte1.MOV",
    "assets/corte2.MOV",
    "assets/corte3.MOV",
    "assets/corte4.MOV"
]
horas = ["","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00"]
servicio = ["","Corte", "Corte + Barba"]
barber = ["", "Juan"]

document = "App-Reservas"
sheet_name = "Reservas"
credentials = st.secrets["credentials"]["credentials"]
calendar_id = "juancholatorre7@gmail.com"
timezone = "America/Buenos_Aires"

#Funciones
def email_validator(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(pattern, email):
        return True
    else:
        return False

def generate_uid():
    return str(uuid.uuid4())

def generate_end_time(time):
    parsed_time = dt.datetime.strptime(time, "%H:%M").time()
    end_time = (dt.datetime.combine(dt.date.today(), parsed_time) + dt.timedelta(hours=1)).time()
    return end_time.strftime("%H:%M")


st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.image("assets/portadaPelu.jpeg")
c1,c2 = st.columns([5, 1])
with c2:
    st.image("assets/latoLogo.png")
with c1:
    st.markdown("<h5 style='margin-top: 10px; font-size: 32px; font-family: Arial, sans-serif;'>Latorre Estudio</h5>", unsafe_allow_html=True)
    st.markdown("<h5 style='margin-top: -10px;font-size: 18px;'>Salón de cortes</h5>", unsafe_allow_html=True)

selected = option_menu(menu_title=None, options=["Reservar", "Cortes", "Ubicacion"], icons=["calendar-date","scissors","geo-alt"], orientation="horizontal")

if selected == "Ubicacion":
   
    st.subheader("Ubicación")
    st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d972.6172538836702!2d-57.924289139776874!3d-34.919460599049565!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95a2e78a5e3e1049%3A0xec44532c4c57364e!2sLatorre%20estudio%20barberia!5e0!3m2!1ses-419!2sar!4v1716583980205!5m2!1ses-419!2sar" width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True)
    
    st.subheader("Horarios")
    dia, hora = st.columns(2)
    
    with dia:
        st.text("Martes a Sabado")
        st.text("Lunes y domingos")
        st.text("Feriados")
        
    with hora:
        st.text("10:00hs a 20:00hs")
        st.text("Cerrado")
        st.text("Consultá por WhatsApp o Instagram")
        
    # st.subheader("Contactanos por WhatsApp!")
    # st.markdown("""<i class="bi bi-whatsapp">3794</i>""",unsafe_allow_html=True)
    
    
    # st.subheader("Redes Sociales")
    # st.markdown("Seguinos en Instagram [@santisanchezdeb](https://www.instagram.com/santisanchezdeb/)!")
    st.subheader("Contactanos")

    # WhatsApp contacto
    whatsapp_logo_url = "https://upload.wikimedia.org/wikipedia/commons/5/5e/WhatsApp_icon.png"
    whatsapp_number = "+2213600197"
    whatsapp_html = f"""
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <img src="{whatsapp_logo_url}" alt="WhatsApp" style="width: 44px; height: 44px; margin-right: 15px;">
        <a href="https://wa.me/{whatsapp_number[1:]}" style="font-size: 20px; text-decoration: none; color: white;">221 360-0197</a>
    </div>
    """
    st.markdown(whatsapp_html, unsafe_allow_html=True)

    # Instagram contacto
    instagram_logo_url = "https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png"
    instagram_username = "_latorrestudio"
    instagram_url = f"https://www.instagram.com/{instagram_username}/"
    instagram_html = f"""
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <img src="{instagram_logo_url}" alt="Instagram" style="width: 40px; height: 40px; margin-right: 15px;">
        <a href="{instagram_url}" style="font-size: 20px; text-decoration: none; color: white;">@{instagram_username}</a>
    </div>
    """
    st.markdown(instagram_html, unsafe_allow_html=True)
    
if selected == "Cortes":
    
    st.subheader("Cortes")
    
    c1, c2 = st.columns(2)
    
    for i, video_path in enumerate(cortes):
        if i % 2 == 0:
            c1.video(video_path)
        else:
            c2.video(video_path)  
 
# if selected == "Contacto":
    
#     st.subheader("Contacto")
#     st.markdown("Seguinos en [Instagram](https://www.instagram.com/_latorrestudio/)!")
#     st.markdown("Por cualquier consulta comunicate al [WhatsApp]()")
    
if selected == "Reservar":
    
    st.subheader("Reserva")
    
    c1,c2 = st.columns(2)
    
    nombre = c1.text_input("Nombre*")
    celular = c2.text_input("Celular*", help="Celular: Por si necesitamos comunicarnos con vos")
    email = c1.text_input("Email*", help="Email: Solo para confirmarte la reserva")
    barber = c2.selectbox("Barber*", barber)
    fecha = c1.date_input("Fecha*", value=None, min_value=date.today(),format="DD/MM/YYYY")
    if fecha:
        if fecha.weekday() == 0 or fecha.weekday() == 6:
            st.warning("Estamos cerrados los lunes y domingos! Por favor, elegí otra fecha")
        elif fecha == date.today():
            st.warning("Para turnos en el dia comunicarse al WhatsApp")
        else:
            calendar = GoogleCalendar(credentials,calendar_id)
            reserved_hours = calendar.get_event_start_time(str(fecha))
            available_hours = np.setdiff1d(horas, reserved_hours)
            horario = c2.selectbox("Horario*", available_hours)
    # servicio = c1.selectbox("Servicio", servicio)
    notas = st.text_area("Notas")
        
    reservar = st.button("Reservar")
    
    if reservar:
        with st.spinner("Cargando..."):
            if not nombre:
                st.warning("El nombre es obligatorio")
            elif not email:
                st.warning("En el mail recibirás la confirmación del turno!")
            elif not email_validator(email):
                st.warning("Ingrese un email válido")
            elif not celular:
                st.warning("Necesitamos tu celular por si tenemos que contactarnos con vos")
            elif not barber:
                st.warning("Elegí quién querés que te corte")
            elif not fecha:
                st.warning("Necesitamos saber cuando te queres cortar el pelo")
            elif not horario:
                st.warning("Necesitamos saber a qué hora queres agendar tu corte")
            else:
                #Crear evento en Google Calendar
                local_tz = pytz.timezone(timezone)
                parsed_time = dt.datetime.strptime(horario, "%H:%M").time()
                start_time_local = local_tz.localize(dt.datetime(fecha.year, fecha.month, fecha.day, parsed_time.hour, parsed_time.minute))
                start_time_utc = start_time_local.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S")
                
                end_hour = generate_end_time(horario)
                
                parsed_end_time = dt.datetime.strptime(end_hour, "%H:%M").time()
                end_time_local = local_tz.localize(dt.datetime(fecha.year, fecha.month, fecha.day, parsed_end_time.hour, parsed_end_time.minute))
                end_time_utc = end_time_local.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S")
                
                calendar = GoogleCalendar(credentials,calendar_id)
                calendar.create_event(nombre,start_time_local.isoformat(),end_time_local.isoformat(),timezone)
                
                #Crear registro Google Sheets
                gs = GoogleSheets(credentials, document, sheet_name)
                uid = generate_uid()
                data = [[nombre,celular,email,barber,str(fecha),horario,notas,uid]]
                range = gs.get_last_row_range()
                gs.write_data(range,data)
                
                #Enviar mail al usuario
                send_email(email,nombre,fecha,horario,barber)
                
                st.success("Su turno fue reservado")
        
            
    
 




