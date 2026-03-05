import streamlit as st
import random

st.set_page_config(page_title="Academy: Expertas en Ventas", page_icon="✨")

st.title("🏆 Simulador de Expertas en Ventas")
st.write("Practica tus argumentos de venta con los productos de nuestros catálogos (COSRX, TOCOBO, G9SKIN, Maxybelt, Echosline, etc.).")

# BASE DE DATOS EXTRAÍDA DE TUS ARCHIVOS
banco_preguntas = {
    "Skincare Coreano": [
        {
            "pregunta": "¿Cuál es el beneficio principal del Low pH Good Morning Gel Cleanser de COSRX?",
            "opciones": ["Limpia sin irritar manteniendo el pH natural", "Es un exfoliante fuerte", "Solo sirve para maquillaje pesado", "No se puede usar de día"],
            "correcta": "Limpia sin irritar manteniendo el pH natural"
        },
        {
            "pregunta": "¿Qué ingrediente estrella tiene la línea de SKIN1004?",
            "opciones": ["Centella Asiática de Madagascar", "Baba de Caracol", "Vitamina C Pura", "Ácido Hialurónico"],
            "correcta": "Centella Asiática de Madagascar"
        }
    ],
    "Cuidado Capilar": [
        {
            "pregunta": "En el catálogo de Maxybelt, ¿para qué se usan los matizantes o intensificadores?",
            "opciones": ["Para atenuar o corregir reflejos no deseados", "Para lavar el cabello profundamente", "Para fijar peinados altos", "Como protector térmico únicamente"],
            "correcta": "Para atenuar o corregir reflejos no deseados"
        }
    ]
}

# SELECCIÓN DE CATEGORÍA
cat = st.selectbox("¿Qué quieres estudiar hoy?", list(banco_preguntas.keys()))

if st.button("Generar Pregunta"):
    st.session_state.pregunta_act = random.choice(banco_preguntas[cat])
    st.session_state.respondido = False

if 'pregunta_act' in st.session_state:
    st.write(f"### {st.session_state.pregunta_act['pregunta']}")
    opcion = st.radio("Tu respuesta:", st.session_state.pregunta_act['opciones'])
    
    if st.button("Enviar Respuesta"):
        if opcion == st.session_state.pregunta_act['correcta']:
            st.success("¡Correcto! Excelente argumento de venta. 🌟")
        else:
            st.error(f"Incorrecto. La respuesta era: {st.session_state.pregunta_act['correcta']}")
