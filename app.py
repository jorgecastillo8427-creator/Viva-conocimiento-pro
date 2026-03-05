import streamlit as st
import random

# Configuración de página
st.set_page_config(page_title="Academy: Entrenamiento de Ventas", page_icon="✨")

# --- BASE DE DATOS COMPLETA (Estructura para 200 preguntas) ---
if 'banco_total' not in st.session_state:
    st.session_state.banco_total = {
        "Nivel Básico": [
            {"marca": "SKIN1004", "pregunta": "¿De dónde proviene la Centella Asiática de esta marca?", "opciones": ["Madagascar", "Seúl", "Jeju", "Amazonas"], "correcta": "Madagascar", "argumento": "Pureza máxima para pieles sensibles."},
            {"marca": "COSRX", "pregunta": "¿Por qué el Low pH Cleanser es para la mañana?", "opciones": ["Porque respeta el pH natural", "Porque despierta la piel", "Porque huele a café", "Porque brilla"], "correcta": "Porque respeta el pH natural", "argumento": "Limpia sin dejar la piel estirada."},
            {"marca": "G9SKIN", "pregunta": "¿Qué hace la línea White in Milk?", "opciones": ["Ilumina e hidrata", "Solo limpia", "Quita el acné", "Es para el pelo"], "correcta": "Ilumina e hidrata", "argumento": "Ideal para pieles opacas con proteína de leche."},
            # ... Aquí agregaremos las demás hasta completar 200
        ],
        "Nivel Intermedio": [
            {"marca": "TOCOBO", "pregunta": "¿Qué efecto tiene el Cica Cooling Sun Stick?", "opciones": ["Reduce temperatura y calma", "Es base de maquillaje", "Es un aceite", "Solo para playa"], "correcta": "Reduce temperatura y calma", "argumento": "Calma la piel roja por el sol al instante."},
            {"marca": "MAXYBELT", "pregunta": "¿Para qué sirven los matizantes?", "opciones": ["Corregir reflejos no deseados", "Alisar", "Crecer el cabello", "Dar perfume"], "correcta": "Corregir reflejos no deseados", "argumento": "Elimina tonos naranjas y amarillos en decoloraciones."},
        ],
        "Nivel Avanzado": [
            {"marca": "ECHOSLINE", "pregunta": "¿Cuál es el fin de la línea Balance?", "opciones": ["Detoxificar el cuero cabelludo", "Dar mucho volumen", "Fijar peinados", "Teñir canas"], "correcta": "Detoxificar el cuero cabelludo", "argumento": "Un cuero cabelludo sano es la base de un cabello hermoso."},
        ]
    }

# --- LÓGICA DE SELECCIÓN Y ALEATORIEDAD ---
st.title("🚀 Entrenamiento de Ventas")

# 1. Filtro de Nivel
nivel = st.sidebar.selectbox("Elige tu nivel:", list(st.session_state.banco_total.keys()))

# 2. Generación Aleatoria de 10 (Sin repeticiones en la sesión)
if st.sidebar.button("Cargar Nuevo Examen (10 preguntas)") or 'examen_actual' not in st.session_state:
    # Toma 10 al azar o el máximo disponible si hay menos de 10
    pool = st.session_state.banco_total[nivel]
    cantidad = min(10, len(pool))
    st.session_state.examen_actual = random.sample(pool, k=cantidad)
    st.session_state.indice = 0
    st.session_state.puntos = 0

# --- INTERFAZ DEL EXAMEN ---
if st.session_state.indice < len(st.session_state.examen_actual):
    pregunta = st.session_state.examen_actual[st.session_state.indice]
    
    st.subheader(f"Pregunta {st.session_state.indice + 1} de {len(st.session_state.examen_actual)}")
    st.info(f"**Marca: {pregunta['marca']}** \n\n {pregunta['pregunta']}")
    
    # 3. Respuesta del usuario
    respuesta = st.radio("Selecciona tu mejor argumento de venta:", pregunta['opciones'], key=f"q_{st.session_state.indice}")
    
    if st.button("Validar y Siguiente"):
        if respuesta == pregunta['correcta']:
            st.success(f"✅ ¡Correcto! {pregunta['argumento']}")
            st.session_state.puntos += 1
        else:
            st.error(f"❌ Incorrecto. La respuesta era: {pregunta['correcta']}")
            st.warning(f"Tip: {pregunta['argumento']}")
        
        st.session_state.indice += 1
        st.rerun()
else:
    st.balloons()
    st.header("🎉 ¡Sesión Terminada!")
    st.metric("Puntaje Final:", f"{st.session_state.puntos} / {len(st.session_state.examen_actual)}")
    if st.button("Empezar otra vez"):
        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.rerun()
