import streamlit as st
import random

# Configuración inicial
st.set_page_config(page_title="Academy: Expertas en Ventas", page_icon="✨")

# Título y Bienvenida
st.title("🏆 Simulador de Expertas en Ventas")
st.markdown("### Bloque 1: Skincare & Capilar (Nivel Básico)")
st.write("Demuestra que conoces los beneficios reales para cerrar más ventas.")

# --- BASE DE DATOS (Basada en tus archivos) ---
if 'banco_preguntas' not in st.session_state:
    st.session_state.banco_preguntas = [
        {
            "marca": "SKIN1004",
            "pregunta": "Clienta: '¿Por qué esta Centella es mejor que otras?'. Tu argumento de venta es:",
            "opciones": [
                "Porque proviene de la naturaleza inmaculada de Madagascar",
                "Porque es fabricada en Estados Unidos",
                "Porque es la más barata del mercado",
                "Porque no tiene olor"
            ],
            "correcta": "Porque proviene de la naturaleza inmaculada de Madagascar",
            "tip": "Venta: El origen de Madagascar garantiza la máxima pureza y potencia del activo."
        },
        {
            "marca": "G9SKIN",
            "pregunta": "¿Qué tres ingredientes hacen que la línea 'White in Milk' sea tan efectiva para aclarar la piel?",
            "opciones": [
                "Niacinamida, Glutatión y Galactomyces",
                "Agua, Jabón y Alcohol",
                "Retinol y Vitamina C pura",
                "Aceite de coco y Limón"
            ],
            "correcta": "Niacinamida, Glutatión y Galactomyces",
            "tip": "Venta: Esta tríada ilumina la piel opaca sin irritarla."
        },
        {
            "marca": "TOCOBO",
            "pregunta": "Clienta: 'Siento la piel caliente por el sol'. ¿Qué beneficio del 'Cica Cooling Sun Stick' mencionas?",
            "opciones": [
                "Que reduce la temperatura de la piel y calma la irritación",
                "Que sirve como sombra de ojos",
                "Que es un aceite bronceador",
                "Que se usa solo antes de dormir"
            ],
            "correcta": "Que reduce la temperatura de la piel y calma la irritación",
            "tip": "Venta: El efecto 'Cooling' es un cierre de venta inmediato en días calurosos."
        },
        {
            "marca": "MAXYBELT",
            "pregunta": "Según tu catálogo, ¿para qué sirven los matizantes en un proceso de coloración?",
            "opciones": [
                "Para atenuar, contrarrestar o corregir reflejos no deseados",
                "Para que el cabello crezca más rápido",
                "Para alisar el cabello permanentemente",
                "Para reemplazar el champú"
            ],
            "correcta": "Para atenuar, contrarrestar o corregir reflejos no deseados",
            "tip": "Venta: Úsalos para vender servicios de corrección de color (quitar naranjas/amarillos)."
        },
        {
            "marca": "ECHOSLINE",
            "pregunta": "¿Cuál es la filosofía de la línea 'Balance' para un cabello sano?",
            "opciones": [
                "Primero un cuero cabelludo limpio, sano y detoxificado",
                "Usar mucha laca y fijador",
                "No lavar el cabello nunca",
                "Usar solo tintes sin lavar"
            ],
            "correcta": "Primero un cuero cabelludo limpio, sano y detoxificado",
            "tip": "Venta: Educa a la clienta: un cabello hermoso nace de una raíz sana."
        }
    ]

# --- LÓGICA DEL SIMULADOR ---
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.puntaje = 0

preguntas = st.session_state.banco_preguntas

if st.session_state.indice < len(preguntas):
    p = preguntas[st.session_state.indice]
    
    st.subheader(f"Pregunta sobre: {p['marca']}")
    st.info(p['pregunta'])
    
    respuesta = st.radio("Elige la opción correcta:", p['opciones'], key=f"r_{st.session_state.indice}")
    
    if st.button("Siguiente Pregunta ➡️"):
        if respuesta == p['correcta']:
            st.success(f"✅ ¡Excelente! {p['tip']}")
            st.session_state.puntaje += 1
        else:
            st.error(f"❌ Incorrecto. La respuesta era: {p['correcta']}")
            st.warning(f"Tip de venta: {p['tip']}")
        
        st.session_state.indice += 1
        st.rerun()

else:
    st.balloons()
    st.title("¡Entrenamiento Completado! 🌟")
    st.metric("Tu puntaje de Vendedora Pro:", f"{st.session_state.puntaje}/{len(preguntas)}")
    if st.button("Reiniciar Entrenamiento"):
        st.session_state.indice = 0
        st.session_state.puntaje = 0
        st.rerun()
