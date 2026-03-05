import streamlit as st
import random

# --- INICIALIZAR ESTADO ---
if 'historial' not in st.session_state:
    st.session_state.historial = []

# --- BASE DE DATOS (Estructura preparada para 200 preguntas) ---
if 'banco_total' not in st.session_state:
    st.session_state.banco_total = {
        "Nivel Básico": [
            {"marca": "SKIN1004", "pregunta": "¿De dónde proviene la Centella Asiática de esta marca?", "opciones": ["Madagascar", "Seúl", "Jeju", "Amazonas"], "correcta": "Madagascar", "argumento": "Pureza máxima para pieles sensibles."},
            {"marca": "COSRX", "pregunta": "¿Por qué el Low pH Cleanser es ideal para la mañana?", "opciones": ["Porque respeta el pH natural", "Porque es muy fuerte", "Porque huele a café", "Porque brilla"], "correcta": "Porque respeta el pH natural", "argumento": "Limpia sin dejar la piel estirada."},
            {"marca": "G9SKIN", "pregunta": "¿Qué beneficio ofrece la línea White in Milk?", "opciones": ["Ilumina e hidrata", "Solo limpia", "Quita el acné", "Es para el pelo"], "correcta": "Ilumina e hidrata", "argumento": "Ideal para pieles opacas con proteína de leche."},

            # --- SKIN1004 ---
            {"marca": "SKIN1004", "pregunta": "¿Cuál es el ingrediente principal de toda la línea de SKIN1004?", "opciones": ["Centella Asiática", "Baba de Caracol", "Ácido Hialurónico", "Vitamina C"], "correcta": "Centella Asiática", "argumento": "Es el corazón de la marca, conocida por calmar y reparar la piel."},
            {"marca": "SKIN1004", "pregunta": "¿De qué lugar proviene la centella de SKIN1004?", "opciones": ["Madagascar", "Isla Jeju", "Amazonas", "Alpes Suizos"], "correcta": "Madagascar", "argumento": "Es considerada la ubicación con la centella más pura del mundo."},
            {"marca": "SKIN1004", "pregunta": "¿Qué beneficio principal ofrece la línea 'Centella' (color amarillo)?", "opciones": ["Calmar e hidratar", "Aclarar manchas", "Quitar arrugas profundas", "Solo para pieles grasas"], "correcta": "Calmar e hidratar", "argumento": "Ideal para pieles sensibles o irritadas que necesitan alivio inmediato."},
            
            # --- COSRX ---
            {"marca": "COSRX", "pregunta": "¿Por qué es famoso el limpiador 'Low pH Good Morning Gel Cleanser'?", "opciones": ["Porque limpia sin romper la barrera natural de la piel", "Porque quita el maquillaje a prueba de agua", "Porque tiene partículas exfoliantes", "Porque se usa solo una vez al mes"], "correcta": "Porque limpia sin romper la barrera natural de la piel", "argumento": "Su pH bajo (5.0-6.0) es similar al de la piel sana."},
            {"marca": "COSRX", "pregunta": "¿Qué porcentaje de mucina de caracol tiene la famosa esencia de COSRX?", "opciones": ["96%", "50%", "10%", "100%"], "correcta": "96%", "argumento": "Es una de las concentraciones más altas del mercado para reparar la textura de la piel."},
            {"marca": "COSRX", "pregunta": "¿Para qué sirve el parche 'Acne Pimple Master Patch'?", "opciones": ["Para absorber la impureza del granito y protegerlo", "Para ocultar manchas de sol", "Para hidratar las ojeras", "Para exfoliar la nariz"], "correcta": "Para absorber la impureza del granito y protegerlo", "argumento": "Evita que la clienta se toque el granito y ayuda a que sane más rápido."},

            # --- TOCOBO ---
            {"marca": "TOCOBO", "pregunta": "¿Cuál es la característica principal de los productos TOCOBO?", "opciones": ["Son Veganos y Cruelty-Free", "Son solo para hombres", "Son productos de farmacia", "No tienen empaques bonitos"], "correcta": "Son Veganos y Cruelty-Free", "argumento": "Un argumento de venta muy fuerte para clientas conscientes del medio ambiente."},
            {"marca": "TOCOBO", "pregunta": "¿Qué acabado deja el 'Cotton Soft Sun Stick' (el azul)?", "opciones": ["Acabado mate y suave", "Acabado muy brillante", "Acabado pegajoso", "Acabado blanco"], "correcta": "Acabado mate y suave", "argumento": "Es el favorito de quienes odian la sensación grasosa en la cara."},
            {"marca": "TOCOBO", "pregunta": "¿Para qué sirve la 'Vita Glazed Lip Mask'?", "opciones": ["Hidratación intensa para labios secos", "Para lavar la cara", "Como rubor", "Para quitar ojeras"], "correcta": "Hidratación intensa para labios secos", "argumento": "Deja los labios con un efecto 'vidriado' y muy hidratados."},

            # --- G9SKIN ---
            {"marca": "G9SKIN", "pregunta": "¿Cuál es el ingrediente 'estrella' de la línea White in Milk?", "opciones": ["Proteína de leche", "Extracto de café", "Aceite de oliva", "Carbón activado"], "correcta": "Proteína de leche", "argumento": "La leche ayuda a suavizar y dar un tono más uniforme a la piel."},
            {"marca": "G9SKIN", "pregunta": "¿Qué beneficio ofrece el 'White in Milk Capsule Toner'?", "opciones": ["Hidratación y aclarado", "Exfoliación fuerte", "Solo limpieza de maquillaje", "Fijador de maquillaje"], "correcta": "Hidratación y aclarado", "argumento": "Sus cápsulas se rompen al contacto para liberar activos aclarantes."},
            
            # --- CAPILAR (Básico) ---
            {"marca": "MAXYBELT", "pregunta": "¿Qué es un matizante según el uso básico profesional?", "opciones": ["Un producto para neutralizar colores no deseados", "Un champú normal", "Un tinte permanente", "Un protector solar"], "correcta": "Un producto para neutralizar colores no deseados", "argumento": "Ideal para clientas rubias que quieren quitar el tono naranja."},
            {"marca": "ECHOSLINE", "pregunta": "¿Qué significa que un producto sea 'Seliàr'?", "opciones": ["Es la línea de lujo basada en aceites preciosos", "Que es para niños", "Que es solo para hombres", "Que es un producto de limpieza profunda"], "correcta": "Es la línea de lujo basada en aceites preciosos", "argumento": "Enfoque en nutrición y brillo extremo para el cabello."},
            {"marca": "MAXYBELT", "pregunta": "¿Para qué tipo de cabello se recomienda la línea de Keratina?", "opciones": ["Cabellos maltratados o procesados", "Cabellos muy grasos", "Solo para cabellos vírgenes", "Para cabello corto"], "correcta": "Cabellos maltratados o procesados", "argumento": "La keratina ayuda a reponer la estructura perdida del cabello."},
            
            # --- PREGUNTAS DE CIERRE DE VENTA ---
            {"marca": "VENTAS", "pregunta": "Si una clienta tiene piel grasa, ¿qué textura de crema le recomiendas?", "opciones": ["Gel o loción ligera", "Crema muy espesa y aceitosa", "Manteca corporal", "Aceite puro"], "correcta": "Gel o loción ligera", "argumento": "Las texturas ligeras se absorben rápido sin tapar los poros."},
            {"marca": "VENTAS", "pregunta": "¿Cuál es el orden básico de una rutina coreana?", "opciones": ["Limpieza - Tónico - Hidratación - Solar", "Solar - Limpieza - Tónico", "Hidratación - Solar - Limpieza", "Tónico - Solar - Hidratación"], "correcta": "Limpieza - Tónico - Hidratación - Solar", "argumento": "El bloqueador solar SIEMPRE es el último paso de día."},
            {"marca": "VENTAS", "pregunta": "¿Cómo explicas el uso de un 'Double Cleanse' (Doble limpieza)?", "opciones": ["Limpiador en aceite primero y luego en base agua", "Lavarse la cara dos veces con jabón", "Usar solo toallitas húmedas", "Lavar la cara con agua caliente"], "correcta": "Limpiador en aceite primero y luego en base agua", "argumento": "El aceite quita el sol y grasa, el jabón limpia el poro."},
            {"marca": "SKIN1004", "pregunta": "¿La línea 'Hyalu-Cica' (color azul) para qué tipo de piel es ideal?", "opciones": ["Pieles deshidratadas y sensibles", "Solo pieles con acné severo", "Solo pieles muy maduras", "Pieles con manchas negras"], "correcta": "Pieles deshidratadas y sensibles", "argumento": "Mezcla Ácido Hialurónico con Centella para hidratar y calmar."},
            {"marca": "TOCOBO", "pregunta": "¿Qué hace el 'AHA BHA Lemon Toner'?", "opciones": ["Exfolia suavemente y da brillo", "Quema la piel", "Es un protector solar", "Se usa como crema hidratante"], "correcta": "Exfolia suavemente y da brillo", "argumento": "Los ácidos frutales quitan las células muertas para una piel radiante."},
            {"marca": "G9SKIN", "pregunta": "¿Qué es el 'Pink Blur Hydrogel Eyepatch'?", "opciones": ["Parches para hidratar y desinflamar ojeras", "Pegatinas para la nariz", "Crema para los pies", "Mascarilla para todo el rostro"], "correcta": "Parches para hidratar y desinflamar ojeras", "argumento": "Forma rápida de refrescar la mirada antes del maquillaje."},
            # --- CLÍNICA DE VENTAS (Situaciones con clientes) ---
            {"marca": "VENTAS", "pregunta": "Clienta: 'Ese bloqueador de TOCOBO es muy pequeño para el precio'. ¿Cómo defiendes la venta?", "opciones": ["Es tecnología coreana premium, rinde mucho y no deja grasa, ahorras en polvos matificantes", "Es que es importado y el dólar subió", "Tiene razón, busque uno más grande en la farmacia", "Es pequeño para que quepa en el bolso solamente"], "correcta": "Es tecnología coreana premium, rinde mucho y no deja grasa, ahorras en polvos matificantes", "argumento": "Venta: Reenfoca el precio hacia el beneficio (ahorro en otros productos y calidad)."},
            {"marca": "VENTAS", "pregunta": "Clienta: '¿Para qué sirve un tónico? Yo solo uso jabón'. Tu respuesta de venta:", "opciones": ["El tónico equilibra el pH y prepara la piel para que la crema sí funcione y no se desperdicie", "Es solo para que la cara huela rico", "Es un paso opcional que casi nadie usa", "Sirve para limpiar lo que el jabón no pudo"], "correcta": "El tónico equilibra el pH y prepara la piel para que la crema sí funcione y no se desperdicie", "argumento": "Venta: Explicar que el tónico hace que el siguiente producto rinda más es un gran gancho."},
            {"marca": "VENTAS", "pregunta": "Si una clienta tiene 'Piel de Fresa' (queratosis pilaris) en los brazos, ¿qué ingrediente del catálogo buscas?", "opciones": ["BHA (Ácido Salicílico) como el de COSRX", "Mucha vitamina C", "Aceite de coco puro", "Solo agua fría"], "correcta": "BHA (Ácido Salicílico) como el de COSRX", "argumento": "Venta: El BHA limpia el poro desde adentro, eliminando la textura rugosa."},
            
            # --- COSRX (Argumentos de peso) ---
            {"marca": "COSRX", "pregunta": "Clienta: 'Tengo manchas de acné que no se van'. ¿Qué producto de COSRX le ofreces primero?", "opciones": ["The Vitamin C 23 Serum", "El parche de granitos", "La crema de hialurónico", "El tónico de limpieza"], "correcta": "The Vitamin C 23 Serum", "argumento": "Venta: La Vitamina C al 23% es un tratamiento de choque para manchas y luminosidad."},
            {"marca": "COSRX", "pregunta": "Clienta: 'Mi piel es muy seca y se descama'. ¿Qué esencia es su mejor aliada?", "opciones": ["Hyaluronic Acid Hydra Power Essence", "BHA Blackhead Liquid", "AHA 7 Whitehead Liquid", "Salicylic Acid Cleanser"], "correcta": "Hyaluronic Acid Hydra Power Essence", "argumento": "Venta: El hialurónico retiene mil veces su peso en agua, es 'comida' para la piel seca."},

            # --- SKIN1004 (Comparativas) ---
            {"marca": "SKIN1004", "pregunta": "¿Cuál es la diferencia entre la línea Amarilla y la Azul de SKIN1004?", "opciones": ["Amarilla es para calmar, Azul es para hidratación profunda (Hyalu-Cica)", "Amarilla es para viejitos, Azul para jóvenes", "No hay diferencia, solo el color del bote", "Azul es para el sol y Amarilla para la noche"], "correcta": "Amarilla es para calmar, Azul es para hidratación profunda (Hyalu-Cica)", "argumento": "Venta: Saber diferenciar líneas por color ayuda a recomendar rápido según la necesidad."},
            {"marca": "SKIN1004", "pregunta": "Clienta: 'Busco un aceite limpiador que no me deje los ojos empañados'. ¿Cuál le das?", "opciones": ["Centella Light Cleansing Oil", "Jabón de manos", "Agua micelar de supermercado", "Cualquier crema hidratante"], "correcta": "Centella Light Cleansing Oil", "argumento": "Venta: Es ligero, se emulsiona con agua y no deja residuo graso ni empaña la vista."},

            # --- TOCOBO (Tendencias) ---
            {"marca": "TOCOBO", "pregunta": "Clienta: '¿El bloqueador en barra se puede usar sobre el maquillaje?'.", "opciones": ["Sí, el Cotton Soft Sun Stick es ideal para retocar sin arruinar el maquillaje", "No, se te va a correr todo", "Solo si no usas base", "Sí, pero solo en la noche"], "correcta": "Sí, el Cotton Soft Sun Stick es ideal para retocar sin arruinar el maquillaje", "argumento": "Venta: El 'retoque sobre el maquillaje' es el principal motivo de compra de este producto."},
            {"marca": "TOCOBO", "pregunta": "¿Qué hace que el 'Bio Watery Sun Cream' sea diferente a un bloqueador normal?", "opciones": ["Tiene textura de suero hidratante y no deja capa blanca", "Que es de color azul", "Que huele a medicina", "Que es resistente al agua de mar por 24 horas"], "correcta": "Tiene textura de suero hidratante y no deja capa blanca", "argumento": "Venta: Ataca el miedo principal de las clientas: quedar como 'mimo' (blancas)."},

            # --- MAXYBELT / ECHOSLINE (Capilar Básico) ---
            {"marca": "MAXYBELT", "pregunta": "Clienta: 'Quiero que mi tinte dure más'. ¿Qué le recomiendas del catálogo?", "opciones": ["Champú y Tratamiento pH Ácido o para color", "Lavarse el pelo con agua muy caliente", "Cualquier champú de limpieza profunda", "No usar acondicionador"], "correcta": "Champú y Tratamiento pH Ácido o para color", "argumento": "Venta: El pH ácido sella la cutícula para que el color no se escape con las lavadas."},
            {"marca": "ECHOSLINE", "pregunta": "Si un cabello está 'chicloso' o muy elástico por decoloración, ¿qué línea buscas?", "opciones": ["Línea de Reconstrucción (Ki Power)", "Línea de Brillo", "Línea de Volumen", "Línea de Rizo"], "correcta": "Línea de Reconstrucción (Ki Power)", "argumento": "Venta: La queratina molecular repara la fibra desde adentro."},
            {"marca": "MAXYBELT", "pregunta": "Clienta: 'Tengo mucho frizz'. ¿Qué producto finalizador le ofreces?", "opciones": ["Silicón o Serum Sellante de puntas", "Laca de fijación fuerte", "Gel para cabello", "Alcohol puro"], "correcta": "Silicón o Serum Sellante de puntas", "argumento": "Venta: El sellado de puntas elimina el frizz y da brillo instantáneo."},

            # --- TRIVIA RÁPIDA DE ACTIVOS ---
            {"marca": "VENTAS", "pregunta": "¿Qué ingrediente es el 'Rey' para cerrar poros y controlar grasa?", "opciones": ["Niacinamida", "Aceite de Argán", "Manteca de Karité", "Vitamina E"], "correcta": "Niacinamida", "argumento": "Venta: Si la clienta dice 'brillo/poros', tú dices 'Niacinamida'."},
            {"marca": "G9SKIN", "pregunta": "¿Qué hace la mascarilla 'Selfie Aesthetic Magazine'?", "opciones": ["Efecto peeling y luminosidad en pocos minutos", "Es solo para tomarse fotos", "Es un maquillaje", "Sirve para dormir con ella"], "correcta": "Efecto peeling y luminosidad en pocos minutos", "argumento": "Venta: Se vende como un 'tratamiento flash' antes de un evento."},
            {"marca": "VENTAS", "pregunta": "Si una clienta tiene piel madura con arrugas, ¿qué ingrediente del catálogo es el más potente?", "opciones": ["Retinol (como el de COSRX)", "Agua de Rosas", "Glicerina", "Extracto de Limón"], "correcta": "Retinol (como el de COSRX)", "argumento": "Venta: El Retinol es el estándar de oro para revertir signos de la edad."},
            
            # (Continuar hasta completar las 50 del bloque básico...)
            {"marca": "TOCOBO", "pregunta": "¿Qué es el 'Aha Bha Lemon Toner'?", "opciones": ["Un tónico exfoliante que ilumina", "Un jugo de limón", "Un jabón corporal", "Una crema de noche"], "correcta": "Un tónico exfoliante que ilumina", "argumento": "Venta: Ayuda a quitar manchas y suavizar la piel rugosa."},
            {"marca": "SKIN1004", "pregunta": "Si la clienta busca una protección solar física para piel muy sensible, ¿cuál recomiendas?", "opciones": ["Air-fere Sunscreen (Amarillo)", "Cualquier spray de playa", "No usar protector", "Un aceite bronceador"], "correcta": "Air-fere Sunscreen (Amarillo)", "argumento": "Venta: Los filtros físicos son mejores para pieles que se irritan con facilidad."},
            {"marca": "COSRX", "pregunta": "¿Para qué sirve el 'Advanced Snail Radiance Dual Essence'?", "opciones": ["Mezcla baba de caracol con niacinamida para brillar y reparar", "Es una base de maquillaje", "Es un bloqueador solar", "Es solo para los ojos"], "correcta": "Mezcla baba de caracol con niacinamida para brillar y reparar", "argumento": "Venta: Es un '2 en 1' que ahorra pasos y da doble beneficio."},
            {"marca": "MAXYBELT", "pregunta": "¿Qué hace el 'Tratamiento con Embrión de Pato'?", "opciones": ["Nutrición profunda para cabellos secos", "Sirve para alisar", "Es un champú", "Se usa para peinar"], "correcta": "Nutrición profunda para cabellos secos", "argumento": "Venta: Un clásico del catálogo para rescatar cabellos opacos."},
            {"marca": "ECHOSLINE", "pregunta": "¿Para qué sirve el 'No Yellow Shampoo'?", "opciones": ["Para neutralizar los reflejos amarillos en canas o rubios", "Para pintar el pelo de amarillo", "Para el cabello negro", "Para la caída del cabello"], "correcta": "Para neutralizar los reflejos amarillos en canas o rubios", "argumento": "Venta: Es el producto 'obligatorio' para cualquier rubio platino."},
            {"marca": "VENTAS", "pregunta": "La clienta dice: 'No tengo tiempo para 10 pasos'. ¿Qué le vendes?", "opciones": ["Una rutina básica de 3 pasos: Limpia, Hidrata, Protege", "Le obligas a llevar los 10", "Que no use nada entonces", "Solo el bloqueador"], "correcta": "Una rutina básica de 3 pasos: Limpia, Hidrata, Protege", "argumento": "Venta: Menos es más. Si le vendes lo básico hoy, volverá por más mañana."},
            {"marca": "G9SKIN", "pregunta": "¿Qué es el 'It Clean Oil Cleansing Stick'?", "opciones": ["Un desmaquillante en barra súper práctico para viajar", "Un desodorante", "Un jabón de barra normal", "Una vela aromática"], "correcta": "Un desmaquillante en barra súper práctico para viajar", "argumento": "Venta: La comodidad de no derramar líquidos en la maleta."},
            {"marca": "SKIN1004", "pregunta": "¿Para qué sirve la 'Poremizing Fresh Ampoule' (color rosado)?", "opciones": ["Para reducir la apariencia de poros dilatados", "Para hidratar pies", "Para el cabello", "Para desmaquillar"], "correcta": "Para reducir la apariencia de poros dilatados", "argumento": "Venta: Contiene sal rosa del Himalaya para limpiar el poro a fondo."},
            {"marca": "MAXYBELT", "pregunta": "¿Qué beneficio tiene el Aceite de Argán en el cabello?", "opciones": ["Aporta brillo, suavidad y vitamina E", "Hace que el cabello se ponga duro", "Sirve para fijar peinados", "Quita el color del tinte"], "correcta": "Aporta brillo, suavidad y vitamina E", "argumento": "Venta: Es el 'oro líquido' para el cabello seco."},
            {"marca": "ECHOSLINE", "pregunta": "La línea 'Seliàr Discipline' ¿para qué tipo de cabello es?", "opciones": ["Para cabellos rebeldes y encrespados (frizz)", "Para cabellos muy finos", "Solo para hombres", "Para cabello corto"], "correcta": "Para cabellos rebeldes y encrespados (frizz)", "argumento": "Venta: Controla el volumen y deja el cabello manejable."},
            {"marca": "VENTAS", "pregunta": "¿Cuál es la mejor forma de probar un producto de skincare en tienda?", "opciones": ["En el dorso de la mano o mandíbula", "En la palma de la mano", "En el antebrazo", "Directo en los labios"], "correcta": "En el dorso de la mano o mandíbula", "argumento": "Venta: El dorso de la mano permite apreciar la textura y absorción rápidamente."},
            {"marca": "COSRX", "pregunta": "El 'Salicylic Acid Daily Gentle Cleanser' ¿es mejor para qué tipo de piel?", "opciones": ["Piel con acné o tendencia a granitos", "Piel extremadamente seca", "Piel de bebé", "Piel madura sin poros"], "correcta": "Piel con acné o tendencia a granitos", "argumento": "Venta: Ayuda a controlar el brote sin ser agresivo."},
            {"marca": "TOCOBO", "pregunta": "¿Qué hace la 'Coconut Clay Cleansing Foam'?", "opciones": ["Limpia profundamente los poros con burbujas de arcilla", "Huele a coco pero no limpia", "Es una crema de cuerpo", "Es un protector solar"], "correcta": "Limpia profundamente los poros con burbujas de arcilla", "argumento": "Venta: Ideal para clientas que sienten la piel 'sucia' o con mucha grasa."},
            {"marca": "MAXYBELT", "pregunta": "¿Para qué sirve la Silicona con Filtro Solar de Maxybelt?", "opciones": ["Para proteger el cabello del daño del sol y dar brillo", "Para peinar con mucha laca", "Para lavar el cabello", "Para fijar el color del tinte"], "correcta": "Para proteger el cabello del daño del sol y dar brillo", "argumento": "Venta: Producto esencial para ir a la playa o piscina."},
           {"marca": "VENTAS", "pregunta": "Si una clienta te pide algo para 'iluminar la cara cansada', buscas:", "opciones": ["Vitamina C o Niacinamida", "Carbón activado", "Mucha crema pesada", "Alcohol"], "correcta": "Vitamina C o Niacinamida", "argumento": "Venta: Son los activos de luminosidad por excelencia."}
                 
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
    
    st.progress(st.session_state.indice / len(st.session_state.examen_actual))
    st.write(f"Pregunta {st.session_state.indice + 1} de {len(st.session_state.examen_actual)}")
    
    st.info(f"**Marca: {pregunta['marca']}** \n\n {pregunta['pregunta']}")
    
    # Mezclar opciones
    opciones_mezcladas = list(pregunta['opciones'])
    random.Random(st.session_state.indice).shuffle(opciones_mezcladas)
    
    respuesta = st.radio("Selecciona tu mejor argumento de venta:", opciones_mezcladas, key=f"q_{st.session_state.indice}")
    
    if st.button("Validar y Siguiente"):
        es_correcta = (respuesta == pregunta['correcta'])
        
        # Guardamos en el historial para mostrar al final
        st.session_state.historial.append({
            "Pregunta": pregunta['pregunta'],
            "Tu respuesta": respuesta,
            "Resultado": "✅" if es_correcta else "❌",
            "Correcta": pregunta['correcta']
        })

        if es_correcta:
            st.success(f"✅ ¡Correcto! {pregunta['argumento']}")
            st.session_state.puntos += 1
        else:
            st.error(f"❌ Incorrecto. La respuesta era: {pregunta['correcta']}")
        
        st.session_state.indice += 1
        st.rerun()

else:
    # --- PANTALLA FINAL ---
    st.balloons()
    st.header("🎉 ¡Sesión Terminada!")
    
    # Mostrar Puntuación con métrica
    st.metric("Puntaje Final", f"{st.session_state.puntos} / {len(st.session_state.examen_actual)}")
    
    # Mostrar tabla de revisión
    st.subheader("📋 Revisión de tus respuestas:")
    st.table(st.session_state.historial)
    
    if st.button("Empezar Nueva Sesión"):
        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.session_state.historial = []
        # Forzar recarga de preguntas
        st.session_state.examen_actual = random.sample(st.session_state.banco_total[nivel], k=min(20, len(st.session_state.banco_total[nivel])))
        st.rerun()
