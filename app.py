
import streamlit as st
import random

# Configuración de la página
st.set_page_config(page_title="Simulador de Ventas - Belleza", page_icon="💄")

# --- BASE DE DATOS DE PREGUNTAS (Enfoque Ventas) ---
banco_preguntas = {
    "Básico": [
        {
            "pregunta": "Clienta: 'Busco un jabón que no me deje la piel estirada'. ¿Por qué recomendarías el Low pH de COSRX?",
            "opciones": [
                "Porque tiene un pH de 5.0 a 6.0 similar al de la piel y no daña la barrera natural.",
                "Porque es el más barato de la tienda.",
                "Porque tiene mucha espuma y fragancia.",
                "Porque se usa solo en las noches."
            ],
            "correcta": "Porque tiene un pH de 5.0 a 6.0 similar al de la piel y no daña la barrera natural.",
            "argumento": "Venta: El pH equilibrado es el mejor argumento para clientas con piel sensible o que odian la sensación de tirantez."
        },
        {
            "pregunta": "Clienta: '¿Para qué sirve la línea White in Milk de G9SKIN?'. Tu respuesta de venta es:",
            "opciones": [
                "Es solo para pieles grasas.",
                "Es una línea aclarante e hidratante gracias a la proteína de leche y niacinamida.",
                "Es un exfoliante fuerte para el cuerpo.",
                "Solo sirve para quitar el maquillaje a prueba de agua."
            ],
            "correcta": "Es una línea aclarante e hidratante gracias a la proteína de leche y niacinamida.",
            "argumento": "Venta: La proteína de leche es un ingrediente 'premium' que comunica suavidad y lujo inmediato."
        }
    ],
    "Intermedio": [
        {
            "pregunta": "Clienta: 'Quiero un protector solar que pueda usar encima del maquillaje sin dañarlo'. ¿Qué le ofreces?",
            "opciones": [
                "Cualquier bloqueador en crema.",
                "Vita Waterproof Sun Stick de TOCOBO por su acabado mate y formato en barra.",
                "La ampolla de Noni de Celimax.",
                "No se puede usar nada encima del maquillaje."
            ],
            "correcta": "Vita Waterproof Sun Stick de TOCOBO por su acabado mate y formato en barra.",
            "argumento": "Venta: El formato en barra es el 'upsell' perfecto para clientas que pasan mucho tiempo fuera de casa."
        },
        {
            "pregunta": "Una clienta pregunta: '¿Qué hace diferente a Skin1004 de otras marcas?'. El argumento clave es:",
            "opciones": [
                "Que es la marca más antigua de Corea.",
                "Que todos sus productos usan Centella Asiática pura de Madagascar.",
                "Que solo tienen productos para el acné.",
                "Que sus envases son de vidrio."
            ],
            "correcta": "Que todos sus productos usan Centella Asiática pura de Madagascar.",
            "argumento": "Venta: 'Madagascar' posiciona el producto como exótico y de alta pureza botánica."
        }
    ],
    "Avanzado": [
        {
            "pregunta": "Clienta con manchas oscuras persistentes. ¿Cómo vendes el suero de Vitamina C de Good Molecules?",
            "opciones": [
                "Diciendo que es agua con color.",
                "Explicando que tiene 8% de Vitamina C avanzada y Ácido Kójico para unificar el tono.",
                "Diciendo que se puede mezclar con cualquier cosa sin cuidado.",
                "Recomendándolo solo para menores de 20 años."
            ],
            "correcta": "Explicando que tiene 8% de Vitamina C avanzada y Ácido Kójico para unificar el tono.",
            "argumento": "Venta: El Ácido Kójico es el ingrediente 'estrella' para combatir manchas solares."
        }
    ]
}

# --- LÓGICA DE LA INTERFAZ ---
st.title("🚀 Entrenamiento de Ventas: Marcas de Belleza")
st.write("Demuestra que conoces tus productos y sabes cómo venderlos.")

# Selección de Nivel (El "Check" que pediste)
nivel_seleccionado = st.radio("Elige tu nivel de capacitación:", ["Básico", "Intermedio", "Avanzado"], horizontal=True)

# Inicializar estado
if 'preguntas_sesion' not in st.session_state or st.button("🔄 Cargar nuevas preguntas"):
    st.session_state.preguntas_sesion = random.sample(banco_preguntas[nivel_seleccionado], len(banco_preguntas[nivel_seleccionado]))
    st.session_state.respuestas_usuario = {}

# Mostrar preguntas
for i, p in enumerate(st.session_state.preguntas_sesion):
    st.subheader(f"Pregunta {i+1}:")
    st.write(p["pregunta"])
    st.session_state.respuestas_usuario[i] = st.radio(f"Selecciona la mejor respuesta de venta para la P{i+1}:", p["options"], key=f"p{i}")

if st.button("Finalizar y Revisar Conocimiento"):
    puntos = 0
    for i, p in enumerate(st.session_state.preguntas_sesion):
        if st.session_state.respuestas_usuario[i] == p["correcta"]:
            st.success(f"✅ Pregunta {i+1}: ¡Excelente argumento! {p['argumento']}")
            puntos += 1
        else:
            st.error(f"❌ Pregunta {i+1}: No es lo ideal. La respuesta era: {p['correcta']}. Tip de venta: {p['argumento']}")
    
    st.metric("Puntaje de Vendedora Pro:", f"{puntos}/{len(st.session_state.preguntas_sesion)}")
