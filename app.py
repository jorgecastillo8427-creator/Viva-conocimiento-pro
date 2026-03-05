import streamlit as st
import random

# Configuración de página
st.set_page_config(page_title="Academy: Entrenamiento de Ventas", page_icon="✨")

# --- BASE DE DATOS (Estructura preparada para 200 preguntas) ---
if 'banco_total' not in st.session_state:
    st.session_state.banco_total = {
        "Nivel Básico": [
            {"marca": "SKIN1004", "pregunta": "¿De dónde proviene la Centella Asiática de esta marca?", "opciones": ["Madagascar", "Seúl", "Jeju", "Amazonas"], "correcta": "Madagascar", "argumento": "Pureza máxima para pieles sensibles."},
            {"marca": "COSRX", "pregunta": "¿Por qué el Low pH Cleanser es ideal para la mañana?", "opciones": ["Porque respeta el pH natural", "Porque es muy fuerte", "Porque huele a café", "Porque brilla"], "correcta": "Porque respeta el pH natural", "argumento": "Limpia sin dejar la piel estirada."},
            {"marca": "G9SKIN", "pregunta": "¿Qué beneficio ofrece la línea White in Milk?", "opciones": ["Ilumina e hidrata", "Solo limpia", "Quita el acné", "Es para el pelo"], "correcta": "Ilumina e hidrata", "argumento": "Ideal para pieles opacas con proteína de leche."},
            # NOTA: Aquí iremos agregando las 50 preguntas de este nivel
        ],
        "Nivel Intermedio": [
            {"marca": "TOCOBO", "pregunta": "¿Qué efecto tiene el Cica Cooling Sun Stick?", "opciones": ["Reduce temperatura y calma", "Es base de maquillaje", "Es un aceite", "Solo para playa"], "correcta": "Reduce temperatura y calma", "argumento": "Calma la piel roja por el sol al instante."},
            {"marca": "MAXYBELT", "pregunta": "¿Para qué sirven los matizantes según el catálogo?", "opciones": ["Corregir reflejos no deseados", "Alisar", "Crecer el cabello", "Dar perfume"], "correcta": "Corregir reflejos no deseados", "argumento": "Elimina tonos naranjas y amarillos en decoloraciones."},
        ],
        "Nivel Avanzado": [
            {"marca": "ECHOSLINE", "pregunta": "¿Cuál es el fin de la línea Balance?", "opciones": ["Detoxificar el cuero cabelludo", "Dar mucho volumen", "Fijar peinados", "Teñir canas"], "correcta": "Detoxificar el cuero cabelludo", "argumento": "Un cuero cabelludo sano es la base de un cabello hermoso."},
        ]
    }

# --- LÓGICA DE SELECCIÓN ---
st.title("🚀 Entrenamiento de Ventas (Sesión de 20)")

# 1. Filtro de Nivel
nivel = st.sidebar.selectbox("Elige tu nivel:", list(st.session_state.banco_total.keys()))

# 2. Generación Aleatoria de 20 (Ajustado)
if st.sidebar.button("Cargar Nueva Sesión (20 preguntas)") or 'examen_actual' not in st.session_state:
    pool = st.session_state.banco_total[nivel]
    # Si el nivel tiene menos de 20, toma las que haya. Si tiene más, toma 20 exactas al azar.
    cantidad_objetivo = 20
    cantidad_real = min(cantidad_objetivo, len(pool))
    st.session_state.examen_actual = random.sample(pool, k=cantidad_real)
    st.session_state.indice = 0
    st.session_state.puntos = 0

# --- INTERFAZ DEL EXAMEN ---
if st.session_state.indice < len(st.session_state.examen_actual):
    pregunta = st.session_state.examen_actual[st.session_state.indice]
    
    # Barra de progreso
    progreso = (st.session_state.indice) / len(st.session_state.examen_actual)
    st.progress(progreso)
    st.write(f"Pregunta {st.session_state.indice + 1} de {len(st.session_state.examen_actual)}")
    
    st.info(f"**Marca: {pregunta['marca']}** \n\n {pregunta['pregunta']}")
    
    # Respuesta del usuario
    respuesta = st.radio("Selecciona tu mejor argumento de venta:", pregunta['opciones'], key=f"q_{st.session_state.indice}")
    
    if st.button("Validar y Siguiente"):
        if respuesta == pregunta['correcta']:
            st.success(f"✅ ¡Correcto! {pregunta['argumento']}")
            st.session_state.puntos += 1
        else:
            st.error(f"❌ Incorrecto. La respuesta era: {pregunta['correcta']}")
            st.warning(f"Tip de venta: {pregunta['argumento']}")
        
        st.session_state.indice += 1
        # Pequeña pausa para que vean el feedback antes de recargar
        st.rerun()
else:
    # Final de la sesión
    st.balloons()
    st.header("🎉 ¡Sesión de 20 Preguntas Terminada!")
    # Cálculo de efectividad
    porcentaje = (st.session_state.puntos / len(st.session_state.examen_actual)) * 100
    st.metric("Puntaje Final:", f"{st.session_state.puntos} / {len(st.session_state.examen_actual)}")
    
    if porcentaje >= 80:
        st.success(f"Efectividad: {porcentaje}% - ¡Eres una Experta Pro! 😎")
    else:
        st.warning(f"Efectividad: {porcentaje}% - ¡Sigue practicando con los catálogos! 📚")
        
    if st.button("Iniciar Nueva Sesión"):
        st.session_state.indice = 0
        st.session_state.puntos = 0
        # Forzar nueva selección al azar
        pool = st.session_state.banco_total[nivel]
        st.session_state.examen_actual = random.sample(pool, k=min(20, len(pool)))
        st.rerun()
