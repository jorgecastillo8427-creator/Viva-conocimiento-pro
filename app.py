import streamlit as st
import pandas as pd
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. IMPORTACIÓN DEL BANCO DE PREGUNTAS (ARCHIVO SEPARADO) ---
try:
    from preguntas import BANCO_PREGUNTAS
except ImportError:
    st.error("Error: No se encontró el archivo 'preguntas.py'. Asegúrate de haberlo creado.")
    st.stop()

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="VIVA Academy", page_icon="🚀", layout="centered")

# --- 3. CONEXIÓN A GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 4. FUNCIÓN PARA ENVÍO DE CORREO (SOLO FALLOS Y NOTA) ---
def enviar_reporte_errores(vendedor, nota, total, detalles, email_supervisor):
    """Envía la calificación y solo las preguntas fallidas al supervisor y gerencia."""
    try:
        config = st.secrets["email"]
        email_emisor = config["user"]
        password = config["password"]
        email_gerencia = config["gerencia"]

        msg = MIMEMultipart()
        msg['From'] = email_emisor
        msg['To'] = email_supervisor
        msg['Cc'] = email_gerencia
        msg['Subject'] = f"Reporte Academy: {vendedor} ({nota}/{total})"

        # Filtrar solo errores
        errores = [d for d in detalles if d['Estado'] == '❌']
        estado_final = "APROBADO" if nota >= 25 else "REPROBADO"
        
        cuerpo = f"RESUMEN DE CERTIFICACIÓN - VIVA ACADEMY\n"
        cuerpo += f"{'='*40}\n"
        cuerpo += f"Vendedor: {vendedor}\n"
        cuerpo += f"Resultado: {nota} / {total}\n"
        cuerpo += f"Estado: {estado_final}\n"
        cuerpo += f"{'='*40}\n\n"
        
        if errores:
            cuerpo += "DETALLE DE PREGUNTAS FALLIDAS:\n"
            for e in errores:
                cuerpo += f"❌ Pregunta: {e['Pregunta']}\n"
                cuerpo += f"   Respuesta del vendedor: {e['Tu Respuesta']}\n"
                cuerpo += f"   Respuesta Correcta: {e['Respuesta Correcta']}\n\n"
        else:
            cuerpo += "¡Excelente! El vendedor no tuvo fallos."

        msg.attach(MIMEText(cuerpo, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_emisor, password)
            server.sendmail(email_emisor, [email_supervisor, email_gerencia], msg.as_string())
        
        return True

    except Exception as e:
        st.error(f"⚠️ Error técnico al enviar correo: {e}")
        return False

# --- 5. INICIALIZACIÓN DE VARIABLES DE SESIÓN ---
keys_to_init = {
    'autenticado': False, 'examen_terminado': False, 'ya_guardado': False,
    'indice': 0, 'puntos': 0, 'hist': [], 'inicio': None, 'nom': None,
    'correo': None, 'sucursal': None, 'examen_actual': None, 'nivel': None,
    'email_enviado': False, 'supervisor_mail': None
}
for key, value in keys_to_init.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- 5. LÓGICA DE LOGIN (CORREGIDA PARA CONTAR INTENTOS) ---
if not st.session_state.autenticado:
    st.title("🔐 Acceso VIVA Academy")
    clave_input = st.text_input("Ingresa tu Clave:", type="password")
    
    if st.button("Ingresar"):
        # Leemos la lista de vendedores autorizados
        df_form = conn.read(worksheet="Form_Responses", ttl=0)
        df_form['clave'] = df_form['clave'].astype(str).str.strip()
        
        # Buscamos la fila que coincida con la clave
        u = df_form[df_form['clave'] == clave_input.strip()]
        
        if not u.empty:
            # 1. Obtenemos los intentos actuales de la fila encontrada
            intentos_actuales = int(u.iloc[0].get('Intentos', 0))
            
            if intentos_actuales >= 3:
                st.error("❌ Has alcanzado el máximo de 3 intentos permitidos.")
            else:
                # 2. SUMAMOS EL INTENTO Y ACTUALIZAMOS EL EXCEL
                df_form.loc[df_form['clave'] == clave_input.strip(), 'Intentos'] = intentos_actuales + 1
                conn.update(worksheet="Form_Responses", data=df_form)
                
                # 3. Cargamos la sesión del vendedor
                st.session_state.update({
                    "autenticado": True,
                    "nom": u.iloc[0]['NOMBRES'],
                    "correo": u.iloc[0]['CORREO DEL VENDEDOR'],
                    "sucursal": u.iloc[0]['SUCURSAL'],
                    "supervisor_mail": u.iloc[0]['Dirección de correo electrónico'], # Columna B
                    "inicio": None,
                    "indice": 0,
                    "puntos": 0,
                    "hist": [],
                    "examen_terminado": False,
                    "ya_guardado": False
                })
                st.rerun()
        else:
            st.error("Clave incorrecta. Verifica con tu supervisor.")
    st.stop()

# --- 7. PANTALLA DE RESULTADOS FINALES ---
if st.session_state.examen_terminado:
    st.title("📋 Resultados de la Evaluación")
    
    puntaje = st.session_state.puntos
    total = len(st.session_state.examen_actual)

    # Mensajes de aprobación según tu solicitud (Variable 25)
    if puntaje >= 25:
        st.balloons()
        st.success(f"### 🎉 felicidades Ceritificaccion Aprobada con EXITO")
    else:
        st.error(f"### ⚠️ Certificacion REPROBADA")
        st.info("comuníquese con su supervisor para su retroalimentación.")

    st.metric("Puntaje Final", f"{puntaje} / {total}")

    # Guardar en Google Sheets (Solo una vez)
    if not st.session_state.ya_guardado:
        try:
            df_res = conn.read(worksheet="Resultados", ttl=0)
            datos = {
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Nombre": st.session_state.nom,
                "Correo": st.session_state.correo,
                "Categoria": st.session_state.nivel,
                "Calificacion": f"{puntaje}/{total}",
                "Estado": "APROBADO" if puntaje >= 25 else "REPROBADO"
            }
            df_final = pd.concat([df_res, pd.DataFrame([datos])], ignore_index=True)
            conn.update(worksheet="Resultados", data=df_final)
            st.session_state.ya_guardado = True
        except:
            st.warning("Aviso: El resultado se mostrará pero no pudo guardarse en la nube.")

    # Envío de Correo Automático a Supervisor y Gerencia
    if not st.session_state.email_enviado:
        if enviar_reporte_errores(st.session_state.nom, puntaje, total, st.session_state.hist, st.session_state.supervisor_mail):
            st.toast("Reporte enviado a supervisión.")
            st.session_state.email_enviado = True

    # Tabla de Retroalimentación Detallada (Aprender del error)
    st.write("### 🧠 Repasa tus respuestas:")
    st.dataframe(st.session_state.hist, use_container_width=True)
    
    if st.button("Salir y Cerrar Sesión"):
        st.session_state.clear()
        st.rerun()
    st.stop()

# --- 8. SELECCIÓN DE EXAMEN ---
if st.session_state.autenticado and st.session_state.examen_actual is None:
    st.title(f"🚀 Hola, {st.session_state.nom}")
    st.write("Selecciona una categoría para comenzar (30 preguntas):")
    
    seleccion = st.selectbox("Categorías:", ["-- Selecciona --"] + list(BANCO_PREGUNTAS.keys()))
    
    if seleccion != "-- Selecciona --":
        if st.button("Iniciar Certificación"):
            pool = BANCO_PREGUNTAS[seleccion]
            # Seleccionamos 30 o el máximo disponible
            st.session_state.examen_actual = random.sample(pool, k=min(30, len(pool)))
            st.session_state.nivel = seleccion
            st.session_state.inicio = datetime.now()
            st.rerun()
    st.stop()

# --- 9. CRONÓMETRO Y FLUJO DEL EXAMEN ---
st_autorefresh(interval=1000, key="viva_timer")

if st.session_state.inicio:
    restante = max(0, 900 - int((datetime.now() - st.session_state.inicio).total_seconds()))
    m, s = divmod(restante, 60)
    st.sidebar.header(f"⏳ {m:02d}:{s:02d}")
    if restante <= 0:
        st.session_state.examen_terminado = True
        st.rerun()

    i = st.session_state.indice
    p_actual = st.session_state.examen_actual[i]

    st.write(f"**Pregunta {i+1} de {len(st.session_state.examen_actual)}**")
    
    # Bloque de pregunta protegido contra traducción automática
    st.markdown(f"""
        <div class="notranslate" style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
            <p style="color: #555; font-size: 0.9em; margin-bottom: 5px;">CATEGORÍA: {p_actual.get('marca', 'GENERAL')}</p>
            <h4 style="margin: 0;">{p_actual['pregunta']}</h4>
        </div>
    """, unsafe_allow_html=True)

    opciones = p_actual['opciones'].copy()
    # Mezclamos las opciones solo una vez por pregunta usando el índice como semilla
    random.Random(i).shuffle(opciones)
    
    respuesta = st.radio("Elige una opción:", opciones, key=f"q_{i}")

    if st.button("Siguiente" if i < len(st.session_state.examen_actual)-1 else "Finalizar Evaluación"):
        # --- NUEVA LÓGICA DE LIMPIEZA ---
        resp_usuario_limpia = str(respuesta).strip().replace("'", "").replace('"', "").lower()
        resp_correcta_limpia = str(p_actual['correcta']).strip().replace("'", "").replace('"', "").lower()
        
        es_correcta = (resp_usuario_limpia == resp_correcta_limpia)
        # -------------------------------
        
        if es_correcta:
            st.session_state.puntos += 1
        
        # Guardamos en el historial para la retroalimentación final
        st.session_state.hist.append({
            "Pregunta": p_actual['pregunta'],
            "Tu Respuesta": respuesta,
            "Estado": "✅" if es_correcta else "❌",
            "Respuesta Correcta": p_actual['correcta'] # Para mostrar al final
        })

        if i == len(st.session_state.examen_actual) - 1:
            st.session_state.examen_terminado = True
        else:
            st.session_state.indice += 1
        st.rerun()