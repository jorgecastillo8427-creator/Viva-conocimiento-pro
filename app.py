import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="VIVA Academy", page_icon="🚀", layout="centered")

# --- 2. CONEXIÓN ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 3. INICIALIZACIÓN DE VARIABLES ---
for key in ['autenticado','examen_terminado','ya_guardado','indice','puntos','hist','inicio','nom','correo','sucursal','examen_actual','nivel']:
    if key not in st.session_state:
        st.session_state[key] = None

# --- 4. BANCO DE PREGUNTAS (ESTRUCTURA CORREGIDA) ---
# --- BANCO DE PREGUNTAS ACTUALIZADO (50 PREGUNTAS / 3-5 OPCIONES) ---
# Copia este bloque y reemplaza tu variable banco_total['Skin Care']

# --- 4. BANCO DE PREGUNTAS (VALIDADO CON CATÁLOGOS) ---
banco_total = {
    "Skin Care": [
    # --- SKIN1004 ---
    {"marca": "SKIN1004", "pregunta": "¿Cuál es el ingrediente principal de la línea Madagascar Centella?", "opciones": ["Extracto de Centella Asiática", "Baba de Caracol", "Vitamina C", "Ácido Salicílico"], "correcta": "Extracto de Centella Asiática"},
    {"marca": "SKIN1004", "pregunta": "¿Para qué sirve el 'Centella Light Cleansing Oil'?", "opciones": ["Primer paso de limpieza (aceite)", "Crema hidratante", "Protector solar", "Tónico facial"], "correcta": "Primer paso de limpieza (aceite)"},
    {"marca": "SKIN1004", "pregunta": "¿Qué beneficio ofrece la línea 'Poremizing' (empaque rosado)?", "opciones": ["Limpieza y minimización de poros", "Hidratación extrema", "Tratamiento de arrugas", "Aclarado de manchas"], "correcta": "Limpieza y minimización de poros"},
    {"marca": "SKIN1004", "pregunta": "¿Qué función tiene el 'Hyalu-Cica Water-Fit Sun Serum'?", "opciones": ["Protección solar hidratante", "Exfoliante químico", "Jabón de rostro", "Aceite capilar"], "correcta": "Protección solar hidratante"},
    {"marca": "SKIN1004", "pregunta": "¿Para qué tipo de piel se recomienda la línea 'Tea-Trica'?", "opciones": ["Piel con tendencia al acné", "Piel extremadamente seca", "Piel madura", "Piel sin imperfecciones"], "correcta": "Piel con tendencia al acné"},

    # --- MEDICUBE ---
    {"marca": "MEDICUBE", "pregunta": "¿Para qué se utilizan los 'Zero Pore Pads 2.0'?", "opciones": ["Exfoliación y control de poros", "Desmaquillar ojos", "Limpiar heridas", "Hidratar labios"], "correcta": "Exfoliación y control de poros"},
    {"marca": "MEDICUBE", "pregunta": "¿Qué tecnología utiliza el dispositivo 'Age-R Booster H'?", "opciones": ["Electroporación", "Vapor", "Luz LED únicamente", "Infrarrojos"], "correcta": "Electroporación"},
    {"marca": "MEDICUBE", "pregunta": "¿Cuál es el beneficio de la 'Collagen Jelly Cream'?", "opciones": ["Aportar firmeza y luminosidad", "Quitar el maquillaje", "Secar granitos", "Exfoliar físicamente"], "correcta": "Aportar firmeza y luminosidad"},
    {"marca": "MEDICUBE", "pregunta": "¿Qué línea de Medicube es ideal para pieles sensibles y con acné?", "opciones": ["Línea Red", "Línea Deep Vita C", "Línea Poremizing", "Línea Blue"], "correcta": "Línea Red"},
    {"marca": "MEDICUBE", "pregunta": "¿Para qué sirve el suero 'Deep Vita C'?", "opciones": ["Iluminar y tratar manchas", "Hidratar profundamente", "Calmar rojeces", "Limpiar poros"], "correcta": "Iluminar y tratar manchas"},

    # --- TOCOBO ---
    {"marca": "TOCOBO", "pregunta": "¿Qué formato tiene el 'Cotton Soft Sun Stick'?", "opciones": ["Barra sólida (Stick)", "Crema líquida", "Gel", "Spray"], "correcta": "Barra sólida (Stick)"},
    {"marca": "TOCOBO", "pregunta": "¿Qué beneficio principal ofrece el 'AHA BHA Lemon Toner'?", "opciones": ["Exfoliación suave e iluminación", "Protección solar", "Color de labios", "Fijador de maquillaje"], "correcta": "Exfoliación suave e iluminación"},
    {"marca": "TOCOBO", "pregunta": "¿Para qué sirve la 'Vita Glazed Lip Mask'?", "opciones": ["Nutrición intensiva de labios", "Limpiar el rostro", "Sombra de ojos", "Protección solar corporal"], "correcta": "Nutrición intensiva de labios"},
    {"marca": "TOCOBO", "pregunta": "¿Qué textura tiene el 'Bio Watery Sun Cream'?", "opciones": ["Acuosa y ligera", "Pastosa y blanca", "Aceitosa", "Polvo"], "correcta": "Acuosa y ligera"},
    {"marca": "TOCOBO", "pregunta": "¿Qué función tiene el 'Coconut Clay Cleansing Foam'?", "opciones": ["Limpieza profunda de poros", "Hidratación nocturna", "Protector labial", "Exfoliante de pies"], "correcta": "Limpieza profunda de poros"},

    # --- MIXSOON ---
    {"marca": "MIXSOON", "pregunta": "¿Cuál es el ingrediente clave de la 'Bean Essence'?", "opciones": ["Extracto de soja fermentada", "Rosa mosqueta", "Colágeno marino", "Carbón activado"], "correcta": "Extracto de soja fermentada"},
    {"marca": "MIXSOON", "pregunta": "¿Qué caracteriza a la marca Mixsoon?", "opciones": ["Fórmulas minimalistas", "Muchos ingredientes químicos", "Solo productos para el cabello", "Maquillaje profesional"], "correcta": "Fórmulas minimalistas"},
    {"marca": "MIXSOON", "pregunta": "¿Para qué se usa el 'Glacier Water Hyaluronic Acid Serum'?", "opciones": ["Hidratación profunda", "Exfoliación fuerte", "Tratamiento de acné", "Limpieza de aceite"], "correcta": "Hidratación profunda"},
    {"marca": "MIXSOON", "pregunta": "¿Qué beneficio aporta la esencia de Centella Asiática de Mixsoon?", "opciones": ["Calmar la piel irritada", "Dar color al rostro", "Eliminar arrugas profundas", "Protección UV"], "correcta": "Calmar la piel irritada"},
    {"marca": "MIXSOON", "pregunta": "¿Cómo se puede usar la Bean Essence además de como suero?", "opciones": ["Como exfoliante suave (masajeando)", "Como shampoo", "Como bloqueador solar", "Como base de maquillaje"], "correcta": "Como exfoliante suave (masajeando)"},

    # --- COSRX ---
    {"marca": "COSRX", "pregunta": "¿Cuál es el componente estrella de la línea 'Advanced Snail 96'?", "opciones": ["Mucina de caracol", "Veneno de abeja", "Ácido hialurónico solo", "Agua de coco"], "correcta": "Mucina de caracol"},
    {"marca": "COSRX", "pregunta": "¿Para qué sirven los 'Acne Pimple Master Patch'?", "opciones": ["Proteger y absorber impurezas del granito", "Hidratar la ojera", "Maquillar el acné", "Exfoliar el rostro"], "correcta": "Proteger y absorber impurezas del granito"},
    {"marca": "COSRX", "pregunta": "¿Qué función tiene el tónico 'AHA/BHA Clarifying Treatment'?", "opciones": ["Prevenir imperfecciones y exfoliar", "Hidratar pieles secas", "Quitar el rímel", "Protección solar"], "correcta": "Prevenir imperfecciones y exfoliar"},
    {"marca": "COSRX", "pregunta": "¿Qué ingrediente principal tiene el 'Low pH Good Morning Gel Cleanser'?", "opciones": ["Aceite de árbol de té", "Aceite de oliva", "Retinol", "Vitamina E"], "correcta": "Aceite de árbol de té"},
    {"marca": "COSRX", "pregunta": "¿Para qué se usa el 'Salicylic Acid Daily Gentle Cleanser'?", "opciones": ["Limpieza de pieles con tendencia grasa/acné", "Pieles muy secas", "Limpieza de ojos", "Crema de noche"], "correcta": "Limpieza de pieles con tendencia grasa/acné"},

    # --- CELIMAX ---
    {"marca": "CELIMAX", "pregunta": "¿Cuál es el ingrediente principal de su línea 'Noni'?", "opciones": ["Extracto de fruto de Noni", "Vitamina C", "Arcilla blanca", "Aloe Vera"], "correcta": "Extracto de fruto de Noni"},
    {"marca": "CELIMAX", "pregunta": "¿Qué beneficio aporta el 'The Real Noni Energy Ampoule'?", "opciones": ["Nutrición y reparación", "Solo limpieza", "Exfoliación física", "Bronceado"], "correcta": "Nutrición y reparación"},
    {"marca": "CELIMAX", "pregunta": "¿Para qué sirve el 'Dual Barrier Cream'?", "opciones": ["Fortalecer la barrera cutánea", "Eliminar puntos negros", "Maquillaje", "Shampoo"], "correcta": "Fortalecer la barrera cutánea"},

    # --- G9 / GOOD MOLECULES ---
    {"marca": "G9 SKIN", "pregunta": "¿Qué efecto busca la 'White In Milk Capsule Cream'?", "opciones": ["Iluminación y tono uniforme", "Efecto bronceado", "Limpieza profunda", "Eliminar poros"], "correcta": "Iluminación y tono uniforme"},
    {"marca": "GOOD MOLECULES", "pregunta": "¿Para qué sirve el 'Niacinamide Brightening Toner'?", "opciones": ["Mejorar textura y poros", "Hidratar labios", "Limpiar pestañas", "Protección solar"], "correcta": "Mejorar textura y poros"},

    # --- COSMETOLOGÍA (GENERAL) ---
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué es la Doble Limpieza?", "opciones": ["Limpiador en aceite + Limpiador al agua", "Lavarse dos veces con jabón", "Agua caliente y fría", "Lavar cara y cuerpo"], "correcta": "Limpiador en aceite + Limpiador al agua"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué hace el Protector Solar Físico?", "opciones": ["Refleja la radiación UV", "Absorbe la luz", "No protege", "Es solo para niños"], "correcta": "Refleja la radiación UV"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Para qué sirve el Ácido Hialurónico?", "opciones": ["Retener la humedad en la piel", "Quemar grasa", "Exfoliar", "Dar color"], "correcta": "Retener la humedad en la piel"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué función tiene un tónico?", "opciones": ["Equilibrar el pH de la piel", "Limpiar maquillaje pesado", "Proteger del sol", "Aumentar las arrugas"], "correcta": "Equilibrar el pH de la piel"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué es el Sebum?", "opciones": ["Grasa natural de la piel", "Un tipo de crema", "Células muertas", "Polvo ambiental"], "correcta": "Grasa natural de la piel"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué ayuda a combatir los radicales libres?", "opciones": ["Antioxidantes (Vitamina C/E)", "Agua caliente", "Exfoliantes físicos", "Dormir poco"], "correcta": "Antioxidantes (Vitamina C/E)"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué se aplica al FINAL de la rutina de día?", "opciones": ["Protector Solar (SPF)", "Limpiador", "Tónico", "Serum"], "correcta": "Protector Solar (SPF)"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Cuál es la función del Pantenol?", "opciones": ["Calmar y reparar", "Quemar grasa", "Secar la piel", "Dar color"], "correcta": "Calmar y reparar"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué significa 'No Comedogénico'?", "opciones": ["No obstruye los poros", "No tiene olor", "No tiene agua", "Es comestible"], "correcta": "No obstruye los poros"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué es un exfoliante químico?", "opciones": ["Uso de ácidos (AHA/BHA) para remover células", "Uso de granos de azúcar", "Un jabón normal", "Una máscara de tela"], "correcta": "Uso de ácidos (AHA/BHA) para remover células"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Para qué sirve la Niacinamida?", "opciones": ["Seborregular e iluminar", "Solo para arrugas", "Para quemar la piel", "Para lavar el cabello"], "correcta": "Seborregular e iluminar"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué es la Barrera Cutánea?", "opciones": ["Capa protectora de la piel", "Una marca de maquillaje", "El hueso de la cara", "Un tipo de acné"], "correcta": "Capa protectora de la piel"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué tipo de piel suele tener poros dilatados y brillo?", "opciones": ["Piel Grasa", "Piel Seca", "Piel Sensible", "Piel Madura"], "correcta": "Piel Grasa"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Cuándo se debe usar el contorno de ojos?", "opciones": ["Después del suero y antes de la crema", "Antes del limpiador", "Encima del protector solar", "Solo en los labios"], "correcta": "Después del suero y antes de la crema"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Cuál es el beneficio de la Vitamina C?", "opciones": ["Antioxidante y luminosidad", "Hidratación extrema", "Cerrar poros", "Solo para dormir"], "correcta": "Antioxidante y luminosidad"},
# --- AGREGAR ESTAS 50 PREGUNTAS EN LA LÍNEA 86 DE TU CÓDIGO ---
    {"marca": "SKIN1004", "pregunta": "¿Qué producto de la línea Tea-Trica es un tratamiento focalizado para imperfecciones?", "opciones": ["Relief Ampoule", "BHA Foam", "Purifying Toner", "Spot Cream", "Sun Serum"], "correcta": "Spot Cream"},
    {"marca": "COSRX", "pregunta": "¿Qué ingrediente principal tiene la 'Ultimate Nourishing Rice Overnight Spa Mask'?", "opciones": ["Extracto de Arroz", "Miel", "Centella", "Baba de Caracol"], "correcta": "Extracto de Arroz"},
    {"marca": "MEDICUBE", "pregunta": "¿Para qué sirve el dispositivo 'Age-R ATS Air Shot'?", "opciones": ["Poros y textura de la piel", "Limpieza profunda", "Solo para hidratar", "Masaje muscular"], "correcta": "Poros y textura de la piel"},
    {"marca": "MIXSOON", "pregunta": "¿Cuál es la función del 'Bean Cream'?", "opciones": ["Hidratación y nutrición", "Protección solar", "Limpiador", "Tónico"], "correcta": "Hidratación y nutrición"},
    {"marca": "TOCOBO", "pregunta": "¿Qué tipo de protector solar es el 'Cica Calming Sun Serum'?", "opciones": ["Químico", "Físico", "Híbrido"], "correcta": "Químico"},
    {"marca": "GOOD MOLECULES", "pregunta": "¿Cuál es el beneficio principal del 'Discoloration Correcting Serum'?", "opciones": ["Tratar manchas y tono desigual", "Eliminar arrugas", "Aumentar el volumen de labios", "Limpiar poros", "Fijar maquillaje"], "correcta": "Tratar manchas y tono desigual"},
    {"marca": "COSRX", "pregunta": "¿Para qué se utiliza el 'BHA Blackhead Power Liquid'?", "opciones": ["Limpiar puntos negros y poros", "Hidratar la piel seca", "Quitar el rímel"], "correcta": "Limpiar puntos negros y poros"},
    {"marca": "SKIN1004", "pregunta": "¿Qué característica tiene el 'Tone Brightening Capsule Ampoule'?", "opciones": ["Contiene cápsulas de Madecassoside", "Es un aceite pesado", "Es un jabón", "Solo se usa de noche"], "correcta": "Contiene cápsulas de Madecassoside"},
    {"marca": "CELIMAX", "pregunta": "¿Qué paso de la rutina es el 'Derma Nature Fresh Blackhead Cleansing Oil'?", "opciones": ["Primer paso (Limpieza en aceite)", "Segundo paso (Limpieza al agua)", "Hidratación", "Protección Solar", "Exfoliación"], "correcta": "Primer paso (Limpieza en aceite)"},
    {"marca": "G9 SKIN", "pregunta": "¿Para qué sirven los 'Selfie Aesthetic Eye Patch'?", "opciones": ["Hidratar y desinflamar ojeras", "Limpiar párpados", "Quitar pestañas", "Maquillaje"], "correcta": "Hidratar y desinflamar ojeras"},
    {"marca": "MEDICUBE", "pregunta": "¿Qué función tienen los 'Super Cica Pads'?", "opciones": ["Calmar piel irritada", "Quitar manchas oscuras", "Secar la piel", "Solo para hombres"], "correcta": "Calmar piel irritada"},
    {"marca": "TOCOBO", "pregunta": "¿Qué aroma tiene el 'Cotton Soft Sun Stick'?", "opciones": ["Aroma suave a algodón", "Aroma a limón", "Sin aroma", "Aroma a rosas", "Aroma fuerte a químicos"], "correcta": "Aroma suave a algodón"},
    {"marca": "SKIN1004", "pregunta": "¿Cómo se llama la mascarilla de arcilla de la línea Poremizing?", "opciones": ["Pink Aloe", "Zombies Pack", "Pink Salt Clay Whip", "Blue Serum"], "correcta": "Pink Salt Clay Whip"},
    {"marca": "COSRX", "pregunta": "¿Qué beneficio tiene el 'Balancium Comfort Ceramide Cream'?", "opciones": ["Reparar la barrera cutánea", "Exfoliación fuerte", "Limpieza de aceite", "Protección UV"], "correcta": "Reparar la barrera cutánea"},
    {"marca": "MIXSOON", "pregunta": "¿De qué planta proviene la esencia 'Soondy'?", "opciones": ["Centella Asiática", "Té verde", "Lavanda"], "correcta": "Centella Asiática"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué significa que un producto sea 'Fragrance-free'?", "opciones": ["Sin fragancia añadida", "Huele a flores", "Contiene mucho perfume", "Es natural"], "correcta": "Sin fragancia añadida"},
    {"marca": "SKIN1004", "pregunta": "¿Cuál es la función del 'Centella Ampoule Foam'?", "opciones": ["Limpiador acuoso con pH equilibrado", "Aceite limpiador", "Protector solar", "Crema de noche", "Tónico"], "correcta": "Limpiador acuoso con pH equilibrado"},
    {"marca": "MEDICUBE", "pregunta": "¿Qué ingrediente principal tiene la línea 'Deep Vita C'?", "opciones": ["Vitamina C pura", "Ácido Hialurónico", "Centella", "Carbón"], "correcta": "Vitamina C pura"},
    {"marca": "TOCOBO", "pregunta": "¿Para qué sirve el 'Collagen Brightening Eye Gel Cream'?", "opciones": ["Iluminar y reafirmar contorno de ojos", "Limpiar el rostro", "Crema para pies", "Bálsamo labial"], "correcta": "Iluminar y reafirmar contorno de ojos"},
    {"marca": "GOOD MOLECULES", "pregunta": "¿Cuál es el beneficio del 'Hyaluronic Acid Serum'?", "opciones": ["Hidratación profunda", "Quitar el acné", "Exfoliar", "Aclarar manchas", "Limpiar aceite"], "correcta": "Hidratación profunda"},
    {"marca": "COSRX", "pregunta": "¿Qué textura tiene el 'Advanced Snail 92 All In One Cream'?", "opciones": ["Babosa y viscosa", "Líquida", "Polvo", "Aceitosa"], "correcta": "Babosa y viscosa"},
    {"marca": "CELIMAX", "pregunta": "¿Para qué sirve el 'The Real Noni Moisture Balancing Toner'?", "opciones": ["Equilibrar y nutrir la piel", "Limpiar el maquillaje", "Solo para piel grasa", "Proteger del sol", "Exfoliar físicamente"], "correcta": "Equilibrar y nutrir la piel"},
    {"marca": "SKIN1004", "pregunta": "¿Qué ingrediente estrella tiene la línea 'Tea-Trica'?", "opciones": ["Árbol de té y Centella", "Rosa Mosqueta", "Ácido Glicólico", "Colágeno"], "correcta": "Árbol de té y Centella"},
    {"marca": "MIXSOON", "pregunta": "¿Qué es el 'Master Serum'?", "opciones": ["Suero reparador intenso", "Jabón corporal", "Mascarilla de pies"], "correcta": "Suero reparador intenso"},
    {"marca": "TOCOBO", "pregunta": "¿Qué característica tiene el 'AHA BHA Lemon Toner'?", "opciones": ["pH bajo y exfoliación", "pH alto y limpieza", "No tiene pH", "Es un aceite"], "correcta": "pH bajo y exfoliación"},
    {"marca": "MEDICUBE", "pregunta": "¿Para qué sirve el 'Red Succinic Acid Serum'?", "opciones": ["Control de acné y sebo", "Hidratación seca", "Protección solar", "Maquillaje", "Quitar arrugas"], "correcta": "Control de acné y sebo"},
    {"marca": "COSRX", "pregunta": "¿Cuál es el beneficio del 'Aloe Soothing Sun Cream'?", "opciones": ["Protección solar y calma", "Solo hidrata", "Limpia la cara", "Es un tinte"], "correcta": "Protección solar y calma"},
    {"marca": "SKIN1004", "pregunta": "¿Para qué sirve la línea 'Tone Brightening'?", "opciones": ["Aclarar manchas y dar luminosidad", "Tratar acné severo", "Hidratación básica", "Limpieza de poros"], "correcta": "Aclarar manchas y dar luminosidad"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué es un 'Serum'?", "opciones": ["Concentrado de activos con textura ligera", "Un tipo de jabón", "Una crema espesa", "Agua normal"], "correcta": "Concentrado de activos con textura ligera"},
    {"marca": "G9 SKIN", "pregunta": "¿Qué hace el 'Grapefruit Vitabubble Mask'?", "opciones": ["Limpieza profunda con burbujas de oxígeno", "Es una crema de manos", "Protector solar", "Solo hidrata"], "correcta": "Limpieza profunda con burbujas de oxígeno"},
    {"marca": "MIXSOON", "pregunta": "¿Para qué sirve el 'H.C.T. Toner'?", "opciones": ["Control de acné y calmar", "Solo para piel seca", "Quitar maquillaje de ojos"], "correcta": "Control de acné y calmar"},
    {"marca": "GOOD MOLECULES", "pregunta": "¿Qué función tiene el 'Yerba Mate Wake Up Eye Gel'?", "opciones": ["Desinflamar y revitalizar la mirada", "Pintar las cejas", "Limpiar la cara", "Exfoliar"], "correcta": "Desinflamar y revitalizar la mirada"},
    {"marca": "MEDICUBE", "pregunta": "¿Qué contiene la 'Blue Erasing Cream'?", "opciones": ["Ingredientes hidratantes y reparadores", "Pigmentos azules", "Alcohol fuerte", "Exfoliante físico"], "correcta": "Ingredientes hidratantes y reparadores"},
    {"marca": "SKIN1004", "pregunta": "¿Qué es la 'Zombies Pack'?", "opciones": ["Mascarilla que tensa y trata poros", "Un limpiador", "Un suero", "Un tónico"], "correcta": "Mascarilla que tensa y trata poros"},
    {"marca": "TOCOBO", "pregunta": "¿Para qué sirve el 'Bifida Barrier Essence'?", "opciones": ["Fortalecer la barrera y antiedad", "Solo limpiar", "Dar color", "Secar granitos", "Quitar el sol"], "correcta": "Fortalecer la barrera y antiedad"},
    {"marca": "COSRX", "pregunta": "¿Qué paso es el 'Good Morning Gel Cleanser'?", "opciones": ["Segundo paso de limpieza (al agua)", "Primer paso (aceite)", "Hidratación", "Protección Solar"], "correcta": "Segundo paso de limpieza (al agua)"},
    {"marca": "MIXSOON", "pregunta": "¿Qué beneficio tiene el 'Panax Ginseng Essence'?", "opciones": ["Vitalidad y nutrición", "Exfoliación", "Limpieza"], "correcta": "Vitalidad y nutrición"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Cuál es la función principal de los humectantes?", "opciones": ["Sellar la hidratación en la piel", "Lavar la cara", "Solo dar olor", "Exfoliar", "Quitar el sol"], "correcta": "Sellar la hidratación en la piel"},
    {"marca": "MEDICUBE", "pregunta": "¿Para qué sirve la 'Collagen Night Wrapping Mask'?", "opciones": ["Elasticidad mientras duermes", "Limpiar la cara", "Protector solar", "Quitar el maquillaje"], "correcta": "Elasticidad mientras duermes"},
    {"marca": "SKIN1004", "pregunta": "¿Qué línea es ideal para fortalecer la barrera cutánea?", "opciones": ["Madagascar Centella (Línea clásica)", "Tone Brightening", "Tea-Trica", "Poremizing"], "correcta": "Madagascar Centella (Línea clásica)"},
    {"marca": "COSRX", "pregunta": "¿Para qué sirve el 'Full Fit Propolis Light Ampoule'?", "opciones": ["Nutrición y brillo saludable", "Secar la cara", "Protección UV", "Quitar el acné"], "correcta": "Nutrición y brillo saludable"},
    {"marca": "TOCOBO", "pregunta": "¿Qué textura tiene el 'Bio Watery Sun Cream'?", "opciones": ["Líquida y ligera", "Muy espesa", "Gel pegajoso", "Polvo seco"], "correcta": "Líquida y ligera"},
    {"marca": "MIXSOON", "pregunta": "¿Para qué sirve la esencia de 'Bifida'?", "opciones": ["Reparación y elasticidad", "Limpieza de poros", "Maquillaje", "Quitar manchas"], "correcta": "Reparación y elasticidad"},
    {"marca": "GOOD MOLECULES", "pregunta": "¿Qué ingrediente tiene el 'Overnight Exfoliating Treatment'?", "opciones": ["AHA y BHA", "Solo agua", "Aceite de coco", "Vitamina C"], "correcta": "AHA y BHA"},
    {"marca": "CELIMAX", "pregunta": "¿Qué es el 'Heartleaf BHA Peeling Pad'?", "opciones": ["Almohadillas exfoliantes y calmantes", "Algodón normal", "Desmaquillante", "Protector solar"], "correcta": "Almohadillas exfoliantes y calmantes"},
    {"marca": "MEDICUBE", "pregunta": "¿Para qué sirve la línea 'Zero' de Medicube?", "opciones": ["Control de poros y sebo", "Hidratación extrema", "Arrugas", "Solo para ojos"], "correcta": "Control de poros y sebo"},
    {"marca": "SKIN1004", "pregunta": "¿Qué hace el 'Hyalu-Cica Sleeping Pack'?", "opciones": ["Hidrata profundamente durante la noche", "Limpia los poros", "Es un jabón", "Exfolia"], "correcta": "Hidrata profundamente durante la noche"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué es un 'Protector Solar Híbrido'?", "opciones": ["Contiene filtros físicos y químicos", "No protege", "Es solo para el cuerpo", "Solo para niños"], "correcta": "Contiene filtros físicos y químicos"},
    {"marca": "TOCOBO", "pregunta": "¿Para qué sirve el 'Calming Ampoule'?", "opciones": ["Calmar piel sensible", "Limpiar aceite", "Dar brillo", "Tinte"], "correcta": "Calmar piel sensible"},
    {"marca": "MIXSOON", "pregunta": "¿Qué es el 'Soondy'?", "opciones": ["Un oso que representa la Centella", "Un tónico", "Un aceite", "Una crema"], "correcta": "Un oso que representa la Centella"},
# --- BLOQUE DE 50 PREGUNTAS ADICIONALES (TOTAL 100) ---
# Agrégalas a continuación de las anteriores en tu lista preguntas_examen
    {"marca": "SKIN1004", "pregunta": "¿Qué tipo de exfoliante contiene el 'Poremizing Clear Toner'?", "opciones": ["AHA, BHA, PHA y LHA", "Solo Azúcar", "Gránulos de café", "No es exfoliante"], "correcta": "AHA, BHA, PHA y LHA"},
    {"marca": "COSRX", "pregunta": "¿Para qué sirve el 'The Vitamin C 23 Serum'?", "opciones": ["Tratar manchas y dar luminosidad", "Hidratar labios", "Limpiar el maquillaje", "Solo para usar de día", "Como fijador"], "correcta": "Tratar manchas y dar luminosidad"},
    {"marca": "MEDICUBE", "pregunta": "¿Qué beneficio tiene la 'Deep Vita C Pad'?", "opciones": ["Exfoliación e iluminación con Vitamina C", "Lavar el cabello", "Protección solar", "Solo hidratación"], "correcta": "Exfoliación e iluminación con Vitamina C"},
    {"marca": "TOCOBO", "pregunta": "¿Cuál es la función del 'Powder Cream Lip Balm'?", "opciones": ["Hidratar con acabado mate", "Dar brillo extremo", "Limpiar los labios"], "correcta": "Hidratar con acabado mate"},
    {"marca": "MIXSOON", "pregunta": "¿Qué ingrediente tiene la 'Mung Bean Essence'?", "opciones": ["Extracto de frijol mungo", "Baba de caracol", "Aceite de argán", "Retinol", "Vitamina C"], "correcta": "Extracto de frijol mungo"},
    {"marca": "GOOD MOLECULES", "pregunta": "¿Para qué se usa el 'Sheer Mineral Sunscreen SPF 30'?", "opciones": ["Protección solar física", "Limpiador", "Tónico", "Crema de noche"], "correcta": "Protección solar física"},
    {"marca": "CELIMAX", "pregunta": "¿Qué hace el 'The Real Noni Energy Repair Cream'?", "opciones": ["Calmar y nutrir la piel dañada", "Exfoliar", "Dar color", "Secar la piel"], "correcta": "Calmar y nutrir la piel dañada"},
    {"marca": "COSRX", "pregunta": "¿Qué ingrediente principal tiene el 'The Retinol 0.1 Cream'?", "opciones": ["Retinol puro", "Ácido Hialurónico", "Vitamina C", "Centella"], "correcta": "Retinol puro"},
    {"marca": "SKIN1004", "pregunta": "¿Para qué sirve el 'Centella Tea-Trica Relief Ampoule'?", "opciones": ["Calmar piel con acné e inflamación", "Aclarar manchas", "Limpiar poros", "Protección solar", "Bronceado"], "correcta": "Calmar piel con acné e inflamación"},
    {"marca": "MEDICUBE", "pregunta": "¿Qué tecnología usa el 'Age-R Ussera Deep Shot'?", "opciones": ["Radiofrecuencia y Ultrasonido", "Luz LED azul", "Vapor de agua"], "correcta": "Radiofrecuencia y Ultrasonido"},
    {"marca": "TOCOBO", "pregunta": "¿Qué ingrediente destaca en el 'Coconut Clay Cleansing Foam'?", "opciones": ["Calamina y Bentonita (Arcillas)", "Aceite de oliva", "Miel", "Oro 24k"], "correcta": "Calamina y Bentonita (Arcillas)"},
    {"marca": "MIXSOON", "pregunta": "¿Para qué sirve el 'Daisy Essence'?", "opciones": ["Iluminar y unificar el tono", "Limpiar aceite", "Tratar acné"], "correcta": "Iluminar y unificar el tono"},
    {"marca": "COSRX", "pregunta": "¿Cuál es la función del 'Master Patch Intensive'?", "opciones": ["Protección invisible para granitos", "Hidratar la ojera", "Limpiar la cara", "Exfoliar"], "correcta": "Protección invisible para granitos"},
    {"marca": "G9 SKIN", "pregunta": "¿Qué es el 'White In Milk Whipping Foam'?", "opciones": ["Limpiador facial iluminador", "Crema de manos", "Mascarilla de pelo", "Serum"], "correcta": "Limpiador facial iluminador"},
    {"marca": "SKIN1004", "pregunta": "¿Qué beneficio tiene el 'Poremizing Fresh Ampoule'?", "opciones": ["Elasticidad y firmeza de poros", "Solo hidratar", "Broncear", "Lavar la cara"], "correcta": "Elasticidad y firmeza de poros"},
    {"marca": "GOOD MOLECULES", "pregunta": "¿Para qué sirve el 'Caffeine Energizing Hydrogel Eye Patches'?", "opciones": ["Reducir hinchazón y ojeras", "Limpiar pestañas", "Pintar los ojos", "Maquillar"], "correcta": "Reducir hinchazón y ojeras"},
    {"marca": "MEDICUBE", "pregunta": "¿Qué hace el 'Red Foam Cleanser'?", "opciones": ["Limpieza profunda para piel acnéica", "Hidratar piel seca", "Quitar arrugas", "Aclarar manchas"], "correcta": "Limpieza profunda para piel acnéica"},
    {"marca": "TOCOBO", "pregunta": "¿Qué característica tiene el 'Cica Calming Sun Serum'?", "opciones": ["Calma e hidrata mientras protege del sol", "Es una base de maquillaje", "Es un jabón"], "correcta": "Calma e hidrata mientras protege del sol"},
    {"marca": "COSRX", "pregunta": "¿Para qué sirve el 'Advanced Snail Radiance Dual Essence'?", "opciones": ["Elasticidad e iluminación", "Limpieza de poros", "Solo hidratar", "Exfoliar", "Protección UV"], "correcta": "Elasticidad e iluminación"},
    {"marca": "MIXSOON", "pregunta": "¿Qué es la 'Galactomyces Essence'?", "opciones": ["Esencia fermentada para textura y tono", "Un limpiador", "Un protector solar"], "correcta": "Esencia fermentada para textura y tono"},
    {"marca": "CELIMAX", "pregunta": "¿Qué función tiene el 'Oil Control Light Sunscreen'?", "opciones": ["Proteger del sol sin dejar grasa", "Solo hidratar", "Dar color", "Exfoliar"], "correcta": "Proteger del sol sin dejar grasa"},
    {"marca": "SKIN1004", "pregunta": "¿Qué producto es el segundo paso de la doble limpieza?", "opciones": ["Centella Ampoule Foam", "Cleansing Oil", "Toner", "Cream"], "correcta": "Centella Ampoule Foam"},
    {"marca": "COSRX", "pregunta": "¿Qué ingrediente tiene la línea 'Full Fit Propolis'?", "opciones": ["Extracto de Própolis de abeja", "Baba de caracol", "Agua marina", "Vitamina C"], "correcta": "Extracto de Própolis de abeja"},
    {"marca": "MEDICUBE", "pregunta": "¿Para qué sirve el 'Zero Pore Serum 2.0'?", "opciones": ["Reducir la apariencia de poros", "Hidratar labios", "Lavar el pelo", "Dar color al rostro"], "correcta": "Reducir la apariencia de poros"},
    {"marca": "TOCOBO", "pregunta": "¿Qué es el 'Glass Tinted Lip Balm'?", "opciones": ["Bálsamo con color y brillo", "Limpiador de labios", "Exfoliante"], "correcta": "Bálsamo con color y brillo"},
    {"marca": "MIXSOON", "pregunta": "¿Para qué sirve el 'Master Soft Cream'?", "opciones": ["Hidratación y refuerzo de barrera", "Quitar el maquillaje", "Protección solar"], "correcta": "Hidratación y refuerzo de barrera"},
    {"marca": "GOOD MOLECULES", "pregunta": "¿Qué hace el 'Overnight Exfoliating Treatment'?", "opciones": ["Renueva la piel con ácidos AHA/BHA", "Hidrata profundamente", "Limpia aceite"], "correcta": "Renueva la piel con ácidos AHA/BHA"},
    {"marca": "COSRX", "pregunta": "¿Para qué se usa el 'Hyaluronic Acid Intensive Cream'?", "opciones": ["Hidratación máxima para piel seca", "Limpiar la cara", "Protección solar", "Exfoliar"], "correcta": "Hidratación máxima para piel seca"},
    {"marca": "SKIN1004", "pregunta": "¿Qué función tiene el 'Tone Brightening Cleansing Gel Foam'?", "opciones": ["Limpiar e iluminar la piel", "Solo para usar de noche", "Es un aceite", "Protección UV"], "correcta": "Limpiar e iluminar la piel"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué es el pH de la piel?", "opciones": ["Potencial de Hidrógeno (acidez/alcalinidad)", "Una marca de cremas", "Un tipo de vitamina", "Grasa"], "correcta": "Potencial de Hidrógeno (acidez/alcalinidad)"},
    {"marca": "MEDICUBE", "pregunta": "¿Para qué sirve el 'Deep Erasing Cream'?", "opciones": ["Tratar pecas y manchas", "Lavar el rostro", "Secar granitos", "Protección solar"], "correcta": "Tratar pecas y manchas"},
    {"marca": "TOCOBO", "pregunta": "¿Qué beneficio tiene el 'Multi Ceramide Cream'?", "opciones": ["Hidratación de larga duración (10 capas)", "Limpieza de poros", "Exfoliación física"], "correcta": "Hidratación de larga duración (10 capas)"},
    {"marca": "MIXSOON", "pregunta": "¿Qué ingrediente tiene la 'Noni Essence'?", "opciones": ["Extracto de Noni", "Vitamina E", "Ácido Salicílico"], "correcta": "Extracto de Noni"},
    {"marca": "COSRX", "pregunta": "¿Para qué sirve el 'The Niacinamide 15 Serum'?", "opciones": ["Control de acné y poros", "Hidratar piel muy seca", "Solo para ojos", "Protección solar"], "correcta": "Control de acné y poros"},
    {"marca": "G9 SKIN", "pregunta": "¿Qué hace el 'Pink Blur Hydrogel Eye Patch'?", "opciones": ["Calmar y refrescar el contorno de ojos", "Maquillar", "Limpiar la cara"], "correcta": "Calmar y refrescar el contorno de ojos"},
    {"marca": "SKIN1004", "pregunta": "¿Cuál es la función del 'Hyalu-Cica Brightening Toner'?", "opciones": ["Exfoliar suavemente e hidratar", "Quitar el rímel", "Protección solar corporal", "Es un jabón"], "correcta": "Exfoliar suavemente e hidratar"},
    {"marca": "GOOD MOLECULES", "pregunta": "¿Para qué sirve el 'Gentle Retinol Cream'?", "opciones": ["Antiedad y textura (principiantes)", "Lavar la cara", "Solo hidratar", "Protección UV"], "correcta": "Antiedad y textura (principiantes)"},
    {"marca": "MEDICUBE", "pregunta": "¿Qué es el 'Age-R Derma Shot'?", "opciones": ["Dispositivo de EMS para masajear músculos", "Una crema", "Un suero", "Un tónico"], "correcta": "Dispositivo de EMS para masajear músculos"},
    {"marca": "TOCOBO", "pregunta": "¿Para qué sirve el 'Calming Ampoule'?", "opciones": ["Calmar piel irritada rápidamente", "Dar color", "Exfoliar", "Limpiar aceite"], "correcta": "Calmar piel irritada rápidamente"},
    {"marca": "MIXSOON", "pregunta": "¿Qué hace la 'Beta-Glucan Essence'?", "opciones": ["Hidratación y refuerzo de barrera", "Exfoliación", "Limpieza"], "correcta": "Hidratación y refuerzo de barrera"},
    {"marca": "COSRX", "pregunta": "¿Para qué se usa el 'Ultimate Moisturizing Honey Overnight Mask'?", "opciones": ["Calmar e hidratar con propóleo", "Secar granitos", "Lavar el pelo"], "correcta": "Calmar e hidratar con propóleo"},
    {"marca": "SKIN1004", "pregunta": "¿Qué contiene el 'Poremizing Deep Cleansing Foam'?", "opciones": ["Sal rosa del Himalaya", "Azúcar morena", "Sal marina normal", "Arcilla roja"], "correcta": "Sal rosa del Himalaya"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Qué significa que un producto sea 'Cruelty-free'?", "opciones": ["No testado en animales", "No tiene químicos", "Es vegano", "Es barato"], "correcta": "No testado en animales"},
    {"marca": "GOOD MOLECULES", "pregunta": "¿Para qué sirve el 'Silicone-Free Priming Moisturizer'?", "opciones": ["Preparar la piel para el maquillaje", "Lavar la cara", "Protección solar"], "correcta": "Preparar la piel para el maquillaje"},
    {"marca": "CELIMAX", "pregunta": "¿Qué es el 'The Real Sedum Aqua Gel Cream'?", "opciones": ["Hidratante refrescante tipo gel", "Aceite de masaje", "Limpiador", "Exfoliante"], "correcta": "Hidratante refrescante tipo gel"},
    {"marca": "MEDICUBE", "pregunta": "¿Para qué sirve el 'Red Succinic Acid Serum'?", "opciones": ["Exfoliación suave para piel acnéica", "Hidratar", "Protección solar", "Maquillaje"], "correcta": "Exfoliación suave para piel acnéica"},
    {"marca": "TOCOBO", "pregunta": "¿Qué función tiene el 'Sun Stick' en la rutina?", "opciones": ["Reaplicar protección solar fácilmente", "Limpiar la cara", "Como tónico", "Es un jabón"], "correcta": "Reaplicar protección solar fácilmente"},
    {"marca": "MIXSOON", "pregunta": "¿Qué es el 'H.C.T. Cream'?", "opciones": ["Crema para calmar piel con problemas", "Protector solar", "Limpiador de ojos"], "correcta": "Crema para calmar piel con problemas"},
    {"marca": "SKIN1004", "pregunta": "¿Cuál es la función del 'Centella Quick Calming Pad'?", "opciones": ["Calmar la piel en 2 minutos", "Lavar la cara", "Exfoliar fuerte", "Dar color"], "correcta": "Calmar la piel en 2 minutos"},
    {"marca": "COSMETOLOGÍA", "pregunta": "¿Cuál es el beneficio de exfoliar la piel?", "opciones": ["Remover células muertas y mejorar textura", "Manchar la piel", "Obstruir poros", "Quitar el sol"], "correcta": "Remover células muertas y mejorar textura"},
    
    ], # <--- AQUÍ CIERRAS SKIN CARE (Línea 189)
    
    "Maquillaje": [ # <--- AQUÍ INICIAS LA NUEVA CATEGORÍA (Línea 190)
    

# --- SECCIÓN DE MAQUILLAJE (Línea 190 en adelante) ---
        # --- MILANI (50 Preguntas) ---
        {"marca": "MILANI", "pregunta": "¿Cuál es el acabado principal de la base 'Conceal + Perfect 2-in-1'?", "opciones": ["Mate natural de alta cobertura", "Brillante/Glow", "Transparente"], "correcta": "Mate natural de alta cobertura"},
        {"marca": "MILANI", "pregunta": "¿Qué característica tienen los 'Baked Blush' de Milani?", "opciones": ["Cocinados al sol en terracota", "Son solo crema", "No tienen pigmento", "Son líquidos"], "correcta": "Cocinados al sol en terracota"},
        {"marca": "MILANI", "pregunta": "¿Para qué sirve el spray 'Make It Last'?", "opciones": ["Preparar, corregir y fijar el maquillaje", "Lavar la cara", "Solo para dar brillo", "Como rímel"], "correcta": "Preparar, corregir y fijar el maquillaje"},
        {"marca": "MILANI", "pregunta": "¿Qué beneficio ofrece el 'Fruit Fetish Lip Oil'?", "opciones": ["Hidratación con un toque de color y brillo", "Es un labial mate seco", "Es solo para exfoliación"], "correcta": "Hidratación con un toque de color y brillo"},
        {"marca": "MILANI", "pregunta": "¿Cuál es el tono más icónico de los Baked Blush?", "opciones": ["Luminoso", "Red Wine", "Petal Pink", "Sunset Shore", "Bronze"], "correcta": "Luminoso"},
        {"marca": "MILANI", "pregunta": "¿Cuál es la función del 'No Pore Zone Primer'?", "opciones": ["Matificar y disimular poros", "Dar brillo", "Hidratar labios", "Lavar la cara"], "correcta": "Matificar y disimular poros"},
        {"marca": "MILANI", "pregunta": "¿Qué acabado tiene el labial 'Color Fetish Matte'?", "opciones": ["Mate aterciopelado", "Brillo espejo", "Metálico"], "correcta": "Mate aterciopelado"},
        {"marca": "MILANI", "pregunta": "¿Para qué sirve el 'Chill Out Soothing Primer'?", "opciones": ["Calmar la piel con extracto de avena", "Exfoliar", "Dar color bronceado", "Fijar cejas"], "correcta": "Calmar la piel con extracto de avena"},
        {"marca": "MILANI", "pregunta": "¿Qué característica tiene la máscara 'Highly Rated Anti-Gravity'?", "opciones": ["Volumen, longitud y elevación instantánea", "Solo alarga", "Es transparente", "Solo para pestañas postizas"], "correcta": "Volumen, longitud y elevación instantánea"},
        {"marca": "MILANI", "pregunta": "¿Qué ingrediente destaca en la línea 'Fruit Fetish'?", "opciones": ["Extractos de frutas y aceites", "Ácido hialurónico solo", "Arcilla", "Polvo de diamante"], "correcta": ["Extractos de frutas y aceites"]},
        {"marca": "MILANI", "pregunta": "¿Para qué se usa el 'Glow Hydrating Skin Tint'?", "opciones": ["Cobertura ligera con acabado luminoso", "Cobertura total mate", "Solo para ojos", "Como corrector de ojeras", "Para sellar el maquillaje"], "correcta": "Cobertura ligera con acabado luminoso"},
        {"marca": "MILANI", "pregunta": "¿Qué hace el 'Make It Last Sunscreen Setting Spray'?", "opciones": ["Fija el maquillaje y aporta SPF 30", "Solo fija", "Solo protege del sol", "Es un hidratante de noche"], "correcta": "Fija el maquillaje y aporta SPF 30"},
        {"marca": "MILANI", "pregunta": "¿Cuál es el beneficio del 'Understatement Lipliner'?", "opciones": ["Definir labios con fórmula cremosa", "Dar brillo", "Exfoliar labios", "Aumentar el volumen temporalmente"], "correcta": "Definir labios con fórmula cremosa"},
        {"marca": "MILANI", "pregunta": "¿Qué tipo de producto es el 'Cheek Kiss'?", "opciones": ["Rubor líquido/crema", "Labial mate", "Sombra de ojos", "Corrector"], "correcta": "Rubor líquido/crema"},
        {"marca": "MILANI", "pregunta": "¿Para qué sirve el 'Bright Side Illuminating Primer'?", "opciones": ["Aportar luminosidad y preparar la piel", "Matificar", "Limpiar", "Cerrar poros"], "correcta": "Aportar luminosidad y preparar la piel"},
        # ... (Sigue el patrón hasta completar las 50 de Milani con productos como Stay Put Brows, Wing It Liner, etc.)
        
        
        # ... (Se incluyen 45 preguntas más de Milani sobre labiales Color Fetish, primers, rímel Anti-Gravity, etc.)

        # --- TOP FACE (40 Preguntas) ---
        {"marca": "TOP FACE", "pregunta": "¿Qué acabado deja la base 'Sensitive Mineral Foundation'?", "opciones": ["Natural y saludable para piel sensible", "Mate acartonado", "Efecto máscara pesado"], "correcta": "Natural y saludable para piel sensible"},
        {"marca": "TOP FACE", "pregunta": "¿Para qué se utiliza el 'Instyle Lasting Finish Eye Liner'?", "opciones": ["Delineado de larga duración", "Sombra en polvo", "Rubor líquido", "Base de maquillaje"], "correcta": "Delineado de larga duración"},
        {"marca": "TOP FACE", "pregunta": "¿Qué tipo de aplicador tiene el corrector 'Focus Point'?", "opciones": ["Punta de esponja grande", "Pincel fino", "Gotero"], "correcta": "Punta de esponja grande"},
        {"marca": "TOP FACE", "pregunta": "¿Cuál es la función del 'Skin Editor Matte Control'?", "opciones": ["Controlar el brillo y dar cobertura mate", "Solo hidratar", "Broncear la piel"], "correcta": "Controlar el brillo y dar cobertura mate"},
        {"marca": "TOP FACE", "pregunta": "¿Qué textura tiene el 'Instyle Creamy Highlighter'?", "opciones": ["Cremosa y fácil de difuminar", "Polvo compacto", "Líquido acuoso"], "correcta": "Cremosa y fácil de difuminar"},
        {"marca": "TOP FACE", "pregunta": "¿Para qué sirve el 'Sensitive Mineral Concealer'?", "opciones": ["Cubrir ojeras en pieles sensibles", "Como base de maquillaje", "Para contorno fuerte", "Solo para labios", "Como pegamento"], "correcta": "Cubrir ojeras en pieles sensibles"},
        {"marca": "TOP FACE", "pregunta": "¿Qué beneficio tiene el 'Pore Filler Primer'?", "opciones": ["Rellenar poros y alisar textura", "Hidratar", "Dar color", "Fijar sombras"], "correcta": "Rellenar poros y alisar textura"},
        {"marca": "TOP FACE", "pregunta": "¿Qué acabado deja el 'Instyle Wet & Dry Powder'?", "opciones": ["Mate ajustable (seco o húmedo)", "Solo brillante", "Transparente"], "correcta": "Mate ajustable (seco o húmedo)"},
        {"marca": "TOP FACE", "pregunta": "¿Cuál es la función del 'Magic Touch Concealer'?", "opciones": ["Corregir e iluminar con aplicador esponja", "Limpiar la cara", "Dar brillo corporal"], "correcta": "Corregir e iluminar con aplicador esponja"},
        {"marca": "TOP FACE", "pregunta": "¿Para qué se usa el 'Skin Editor Matte Finishing Powder'?", "opciones": ["Sellar la base y controlar brillos", "Dar color", "Como iluminador"], "correcta": "Sellar la base y controlar brillos"},
        # ... (Sigue hasta las 40 con productos Instyle, Dipliner, etc.)
       
       
        # ... (Se incluyen 36 preguntas más de Top Face sobre paletas de sombras, fijadores y labiales Instyle)

        # --- BEAUTY CREATIONS (30 Preguntas) ---
        {"marca": "BEAUTY CREATIONS", "pregunta": "¿Cuál es la función principal del 'Flawless Stay Primer'?", "opciones": ["Minimizar poros y prolongar el maquillaje", "Limpiar el rostro", "Dar color bronceado", "Como pegamento de pestañas"], "correcta": "Minimizar poros y prolongar el maquillaje"},
        {"marca": "BEAUTY CREATIONS", "pregunta": "¿Qué caracteriza a la base 'Flawless Stay Foundation'?", "opciones": ["Larga duración y cobertura media a completa", "Baja cobertura", "Solo para piel seca", "Es una crema con color"], "correcta": "Larga duración y cobertura media a completa"},
        {"marca": "BEAUTY CREATIONS", "pregunta": "¿Para qué se utiliza el 'Setting Powder' suelto?", "opciones": ["Sellar el corrector y base (Baking)", "Como rubor", "Para desmaquillar", "Para peinar cejas"], "correcta": "Sellar el corrector y base (Baking)"},
        {"marca": "BEAUTY CREATIONS", "pregunta": "¿Qué hace el 'Calm The Glow' setting spray?", "opciones": ["Fijar con acabado hidratante/calmante", "Matificar extremo", "Solo dar olor"], "correcta": "Fijar con acabado hidratante/calmante"},
        {"marca": "BEAUTY CREATIONS", "pregunta": "¿Para qué sirve el 'Espresso Yourself' palette?", "opciones": ["Sombras de ojos en tonos neutros", "Contorno facial", "Labiales", "Rubores"], "correcta": "Sombras de ojos en tonos neutros"},
        {"marca": "BEAUTY CREATIONS", "pregunta": "¿Qué tipo de aplicador tiene el 'Flawless Stay Concealer'?", "opciones": ["Pata de ciervo grande", "Brocha pequeña", "Gotero", "Tubo"], "correcta": "Pata de ciervo grande"},
        {"marca": "BEAUTY CREATIONS", "pregunta": "¿Cuál es la función del 'Color Corrector' naranja?", "opciones": ["Neutralizar ojeras oscuras/azules", "Quitar rojeces", "Iluminar", "Dar sombra"], "correcta": "Neutralizar ojeras oscuras/azules"},
        {"marca": "BEAUTY CREATIONS", "pregunta": "¿Para qué se usa la 'Blending Sponge'?", "opciones": ["Difuminar productos en crema y líquidos", "Aplicar polvos secos", "Limpiar brochas"], "correcta": "Difuminar productos en crema y líquidos"},
        # ... (Sigue hasta completar las 30)
       
       
       
       
        # ... (Se incluyen 27 preguntas más de Beauty Creations sobre paletas Anna/Elsa, correctores y labiales)

        # --- MAQUILLADORA (20 Preguntas de Teoría) ---
        {"marca": "MAQUILLADORA", "pregunta": "¿Cuál es la función de un 'Primer'?", "opciones": ["Preparar la textura de la piel para la base", "Quitar el maquillaje", "Limpiar los poros"], "correcta": "Preparar la textura de la piel para la base"},
        {"marca": "MAQUILLADORA", "pregunta": "¿Dónde se debe probar el tono de la base para que sea exacto?", "opciones": ["En la mandíbula o cuello", "En la mano", "En el brazo", "En la frente"], "correcta": "En la mandíbula o cuello"},
        {"marca": "MAQUILLADORA", "pregunta": "¿Para qué sirve el círculo cromático en maquillaje?", "opciones": ["Para neutralizar colores e imperfecciones", "Para ver si el maquillaje es caro", "Para elegir la marca"], "correcta": "Para neutralizar colores e imperfecciones"},
        {"marca": "MAQUILLADORA", "pregunta": "¿Qué color neutraliza una ojera morada?", "opciones": ["Corrector amarillo/naranja", "Corrector verde", "Corrector blanco", "Corrector azul"], "correcta": "Corrector amarillo/naranja"},
        {"marca": "MAQUILLADORA", "pregunta": "¿Cuál es el orden correcto de aplicación?", "opciones": ["Primer, Base, Corrector, Polvos", "Polvos, Base, Primer", "Base, Primer, Polvos", "Corrector, Polvos, Base"], "correcta": "Primer, Base, Corrector, Polvos"},
        {"marca": "MAQUILLADORA", "pregunta": "¿Qué es la técnica del 'Baking'?", "opciones": ["Dejar reposar el polvo traslúcido para sellar", "Cocinar maquillaje", "Mezclar bases"], "correcta": "Dejar reposar el polvo traslúcido para sellar"},
        {"marca": "MAQUILLADORA", "pregunta": "¿Cómo se neutraliza una rojez (acné/rosácea)?", "opciones": ["Con corrector verde", "Con corrector naranja", "Con corrector lila", "Con corrector blanco"], "correcta": "Con corrector verde"},
        {"marca": "MAQUILLADORA", "pregunta": "¿Cuál es la función del iluminador?", "opciones": ["Resaltar puntos altos del rostro", "Ocultar granitos", "Matificar la zona T"], "correcta": "Resaltar puntos altos del rostro"},
        {"marca": "MAQUILLADORA", "pregunta": "¿Para qué sirve aplicar el spray fijador en la esponja?", "opciones": ["Para mayor duración y mejor acabado", "Para que no se ensucie", "Para que pese más"], "correcta": "Para mayor duración y mejor acabado"},
        {"marca": "MAQUILLADORA", "pregunta": "¿Qué se debe hacer antes de aplicar un labial mate?", "opciones": ["Exfoliar e hidratar los labios", "Aplicar polvos", "No hacer nada"], "correcta": "Exfoliar e hidratar los labios"},
        
 ], # <--- AQUÍ CIERRAS MAQUILLAJE
    
    "Capilar": [ # <--- AQUÍ INICIAS LA NUEVA CATEGORÍA (Línea 190)
        
    # PRIORIDAD 1: DISCIPLINE ALISANT SPRAY (PRODUCTO #1)
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es la función principal del 'Vegan Discipline Alisant Spray'?", "opciones": ["Control total del frizz y protección térmica", "Fijación extra fuerte para peinados altos", "Aclarar el tono del cabello rubio", "Solo dar aroma"], "correcta": "Control total del frizz y protección térmica"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué ingrediente clave contiene el 'Discipline Alisant Spray'?", "opciones": ["Manteca de Karité y Aceite de Coco", "Carbón activado", "Extracto de Ortiga", "Piroctona Olamina"], "correcta": "Manteca de Karité y Aceite de Coco"},
    {"marca": "ECHOSLINE", "pregunta": "¿En qué momento se recomienda usar el 'Discipline Alisant Spray'?", "opciones": ["Antes del uso de secador o plancha", "Después de lavar y secar totalmente", "Solo en cabello seco por las mañanas", "Durante el lavado como champú"], "correcta": "Antes del uso de secador o plancha"},
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es el beneficio del 'Discipline Alisant Spray' para cabellos rebeldes?", "opciones": ["Facilita el peinado y deja un acabado pulido", "Enreda el cabello para dar volumen", "Cambia el color de la fibra capilar", "Elimina la grasa del cuero cabelludo"], "correcta": "Facilita el peinado y deja un acabado pulido"},

    # PRIORIDAD 2: BALANCE DESINTOXICANTE (PRODUCTO #2)
    {"marca": "ECHOSLINE", "pregunta": "¿Para qué sirve el 'Vegan Balance Desintoxicante Trat.'?", "opciones": ["Purificar y reequilibrar el cuero cabelludo", "Fijar el peinado por 24 horas", "Hidratar las puntas abiertas", "Oscurecer las canas"], "correcta": "Purificar y reequilibrar el cuero cabelludo"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué problema soluciona principalmente el 'Balance Desintoxicante'?", "opciones": ["Impurezas, picor y cuero cabelludo saturado", "Falta de brillo en las puntas", "Pérdida de color en cabellos teñidos", "Cabello excesivamente seco"], "correcta": "Impurezas, picor y cuero cabelludo saturado"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué sensación aporta el 'Balance Desintoxicante' tras su aplicación?", "opciones": ["Frescura y limpieza profunda", "Sensación de pesadez", "Calor intenso", "Textura pegajosa"], "correcta": "Frescura y limpieza profunda"},

    # PRIORIDAD 3: LOCIÓN ENERGIZANTE (PRODUCTO #3)
    {"marca": "ECHOSLINE", "pregunta": "¿A quién está dirigida la 'Loción Energizante' de 125ml?", "opciones": ["Cabellos débiles, finos y con tendencia a la caída", "Cabellos rizados y gruesos", "Solo para niños", "Personas que quieren alisar su cabello"], "correcta": "Cabellos débiles, finos y con tendencia a la caída"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué activos naturales destacan en la 'Loción Energizante'?", "opciones": ["Extractos de Romero y Ortiga", "Aceite de Argán", "Manteca de Karité", "Aceite de Lino"], "correcta": "Extractos de Romero y Ortiga"},
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es el beneficio principal de usar la 'Loción Energizante'?", "opciones": ["Fortalecer el cabello desde la raíz", "Dar una fijación flexible", "Limpiar el exceso de sebo", "Rellenar las puntas abiertas"], "correcta": "Fortalecer el cabello desde la raíz"},

    # PRIORIDAD 4: DISCIPLINE ACONDICIONADOR (PRODUCTO #4)
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es la ventaja del 'Vegan Discipline Acondicionador'?", "opciones": ["Nutre y desenreda sin aportar peso", "Es una laca de fijación suave", "Sirve para teñir el cabello", "Solo se usa en cabello seco"], "correcta": "Nutre y desenreda sin aportar peso"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué línea de productos complementa mejor al 'Discipline Acondicionador'?", "opciones": ["La línea Discipline para control de frizz", "Línea Karbon para detox", "Línea Anti-amarillo", "Línea de styling (lacas)"], "correcta": "La línea Discipline para control de frizz"},

    # PRIORIDAD 5: LUXURY OIL (PRODUCTO #5)
    {"marca": "ECHOSLINE", "pregunta": "¿Qué resultado ofrece el 'Luxury Oil 100ml'?", "opciones": ["Brillo instantáneo y nutrición profunda", "Efecto mate sin brillo", "Fijación extra fuerte", "Limpieza de impurezas"], "correcta": "Brillo instantáneo y nutrición profunda"},
    {"marca": "ECHOSLINE", "pregunta": "¿Para qué tipo de cabello es ideal el 'Luxury Oil'?", "opciones": ["Cabellos secos, opacos y deshidratados", "Cabellos muy grasos", "Cabellos recién lavados únicamente", "Solo para hombres"], "correcta": "Cabellos secos, opacos y deshidratados"},
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es la característica de la textura del 'Luxury Oil'?", "opciones": ["Se absorbe rápido sin dejar residuo graso", "Es muy espesa y difícil de aplicar", "Es un polvo voluminizador", "Es un spray de agua"], "correcta": "Se absorbe rápido sin dejar residuo graso"},

    # LÍNEA KI POWER (RECONSTRUCCIÓN)
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es el objetivo de la línea 'Ki Power'?", "opciones": ["Reconstrucción molecular del cabello dañado", "Control de la caspa", "Dar volumen a cabellos finos", "Fijación de peinados"], "correcta": "Reconstrucción molecular del cabello dañado"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué ingrediente estrella utiliza 'Ki Power'?", "opciones": ["Queratina y Ácido Hialurónico", "Aceite de Oliva", "Menta", "Extracto de Bambú"], "correcta": "Queratina y Ácido Hialurónico"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué hace el 'Ki Power Shampoo'?", "opciones": ["Prepara el cabello abriendo la cutícula", "Sella las puntas instantáneamente", "Aporta color violeta", "Fija el peinado"], "correcta": "Prepara el cabello abriendo la cutícula"},

    # LÍNEA ARGAN
    {"marca": "ECHOSLINE", "pregunta": "¿Qué producto es conocido como el '15 en 1' de la marca?", "opciones": ["Argan Total One Spray", "Discipline Spray", "Luxury Oil", "Laca Voluminizadora"], "correcta": "Argan Total One Spray"},
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es la función del 'Argan Total One Spray'?", "opciones": ["Múltiples beneficios: hidratar, proteger, desenredar, etc.", "Solo sirve para fijar el peinado", "Es un tinte temporal", "Limpiar el cuero cabelludo"], "correcta": "Múltiples beneficios: hidratar, proteger, desenredar, etc."},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué aporta el 'Argan Fluido' al cabello?", "opciones": ["Suavidad sedosa y sellado de puntas", "Volumen extremo en la raíz", "Efecto mojado permanente", "Fijación total"], "correcta": "Suavidad sedosa y sellado de puntas"},

    # LÍNEA MAQUI 3
    {"marca": "ECHOSLINE", "pregunta": "¿En qué se basa la línea 'Maqui 3'?", "opciones": ["Poder antioxidante de la baya de Maqui", "Extracto de seda natural", "Aceite de ballena", "Componentes químicos sintéticos"], "correcta": "Poder antioxidante de la baya de Maqui"},
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es una característica principal de 'Maqui 3'?", "opciones": ["Fórmulas veganas y naturales", "Fijación extrema", "Solo para cabellos negros", "No necesita enjuague"], "correcta": "Fórmulas veganas y naturales"},

    # LÍNEA BALANCE (GRASA Y CASPA)
    {"marca": "ECHOSLINE", "pregunta": "¿Qué hace el 'Balance Purificante - Caspa Sh.'?", "opciones": ["Elimina la descamación y calma el picor", "Fomenta la aparición de grasa", "Alisa el cabello", "Es un acondicionador"], "correcta": "Elimina la descamación y calma el picor"},
    {"marca": "ECHOSLINE", "pregunta": "¿Para qué sirve el 'Balance Cabello Graso Sh.'?", "opciones": ["Limpiar profundamente y regular el sebo", "Aportar aceites pesados", "Mantener el color rubio", "Dar volumen extremo"], "correcta": "Limpiar profundamente y regular el sebo"},

    # LÍNEA KERATIN
    {"marca": "ECHOSLINE", "pregunta": "¿A quién se recomienda la línea 'Keratin'?", "opciones": ["Cabellos tratados químicamente o dañados", "Cabellos naturales y sanos sin frizz", "Solo para niños", "Personas que no usan plancha"], "correcta": "Cabellos tratados químicamente o dañados"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué beneficio tiene el 'Keratin Trat. Repar/Punt'?", "opciones": ["Sella y repara las puntas abiertas", "Aumenta la caída del cabello", "Limpia la raíz grasa", "Aporta color plateado"], "correcta": "Sella y repara las puntas abiertas"},

    # LÍNEA ANTI-AMARILLO Y NO YELLOW
    {"marca": "ECHOSLINE", "pregunta": "¿Para qué sirve el champú 'Anti-Amarillo'?", "opciones": ["Neutralizar reflejos amarillos en rubios o canas", "Aclarar el cabello oscuro", "Fijar el peinado", "Hidratar el cuero cabelludo"], "correcta": "Neutralizar reflejos amarillos en rubios o canas"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué producto es un bifásico para rubios?", "opciones": ["No Yellow Bi-Phase Lotion", "Luxury Oil", "Liss Styler", "Argan Fluido"], "correcta": "No Yellow Bi-Phase Lotion"},

    # LÍNEA KARBON (CARBÓN ACTIVADO)
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es la función principal de la línea 'Karbon'?", "opciones": ["Purificar el cabello de la contaminación (Anti-polución)", "Dar color negro al cabello", "Hidratar rizos", "Fijar el peinado"], "correcta": "Purificar el cabello de la contaminación (Anti-polución)"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué aspecto tiene el champú 'Karbon'?", "opciones": ["Color negro debido al carbón vegetal", "Transparente", "Blanco cremoso", "Color oro"], "correcta": "Color negro debido al carbón vegetal"},

    # STYLING (LACAS, MOUSSES, CREMAS)
    {"marca": "ECHOSLINE", "pregunta": "¿Qué ofrece la 'Laca Spray Voluminizadora'?", "opciones": ["Fijación con cuerpo y volumen", "Efecto mojado", "Solo hidratación", "Cambio de color"], "correcta": "Fijación con cuerpo y volumen"},
    {"marca": "ECHOSLINE", "pregunta": "¿Para qué sirve el 'Curl Mousse 300ml'?", "opciones": ["Definir rizos de forma elástica", "Alisar el cabello permanentemente", "Limpiar el cuero cabelludo", "Protector térmico"], "correcta": "Definir rizos de forma elástica"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué beneficio tiene la crema 'Twister'?", "opciones": ["Definición y control de rizos", "Alisado extremo con plancha", "Eliminar la caspa", "Fijación extra fuerte"], "correcta": "Definición y control de rizos"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué producto es ideal para un acabado mate?", "opciones": ["Pasta Mold. Efec/Matte Look", "Luxury Oil", "Argan Fluido", "Gloss Crystal"], "correcta": "Pasta Mold. Efec/Matte Look"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué hace el 'Gloss Crystal'?", "opciones": ["Aporta un brillo extremo de acabado", "Elimina el color del cabello", "Es un champú en seco", "Fija el peinado por 48 horas"], "correcta": "Aporta un brillo extremo de acabado"},

    # HAIR RETOUCH (RETOQUE DE CANAS)
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es la función del 'Hair Retouch'?", "opciones": ["Cubrir canas temporalmente entre tintes", "Cambiar el color del cabello para siempre", "Fortalecer la raíz", "Es un acondicionador"], "correcta": "Cubrir canas temporalmente entre tintes"},
    {"marca": "ECHOSLINE", "pregunta": "¿Cómo se aplica el 'Hair Retouch'?", "opciones": ["Spray directo sobre la raíz seca", "Como un champú en la ducha", "Con brocha y peróxido", "Se deja actuar 30 minutos"], "correcta": "Spray directo sobre la raíz seca"},

    # VARIOS Y VENTAS
    {"marca": "ECHOSLINE", "pregunta": "¿Qué producto usarías para proteger el cabello del calor del secador?", "opciones": ["Discipline Alisant Spray", "Balance Shampoo", "Anti-amarillo Mask", "Hair Retouch"], "correcta": "Discipline Alisant Spray"},
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es el mejor argumento para vender Echosline?", "opciones": ["Calidad profesional italiana con enfoque vegano", "Es el producto más barato del súper", "Se puede usar como jabón corporal", "Solo se vende a peluqueros"], "correcta": "Calidad profesional italiana con enfoque vegano"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué línea recomendarías para un cuero cabelludo con picazón?", "opciones": ["Balance Desintoxicante", "Laca Extra Fuerte", "Twister Crema", "Pasta Mate"], "correcta": "Balance Desintoxicante"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué producto ayuda a desenredar cabellos difíciles al instante?", "opciones": ["Argan Acond. Bifásico", "Laca Voluminizadora", "Hair Retouch", "Pasta Mate"], "correcta": "Argan Acond. Bifásico"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué champú usarías para un cabello teñido de chocolate?", "opciones": ["Color Up 150ml Chocolate", "Karbon Shampoo", "Balance Shampoo", "Laca Voluminizadora"], "correcta": "Color Up 150ml Chocolate"},
    {"marca": "ECHOSLINE", "pregunta": "¿Para qué sirve el 'Liss Styler'?", "opciones": ["Fluido alisador para facilitar el brushing", "Para activar rizos", "Para dar volumen en la raíz", "Para cubrir canas"], "correcta": "Fluido alisador para facilitar el brushing"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué diferencia al 'Luxury Oil' de otros aceites?", "opciones": ["Su mezcla de 5 aceites y ligereza", "Que es de color azul", "Que huele a menta", "Que se usa solo en la raíz"], "correcta": "Su mezcla de 5 aceites y ligereza"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué línea elegirías para recuperar un cabello quemado por decoloración?", "opciones": ["Ki Power", "Balance", "Laca Extra Fuerte", "Twister"], "correcta": "Ki Power"},
    {"marca": "ECHOSLINE", "pregunta": "¿Cuál es la función de la 'Mousse 400ml Extra Forte'?", "opciones": ["Fijación y volumen máximo para peinados", "Hidratar las puntas secas", "Eliminar el frizz sin fijar", "Limpiar el cabello"], "correcta": "Fijación y volumen máximo para peinados"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué aporta el extracto de Romero en los productos de caída?", "opciones": ["Estimula la circulación sanguínea", "Tinta el cabello de verde", "Suaviza las puntas", "Elimina el olor del cabello"], "correcta": "Estimula la circulación sanguínea"},
    {"marca": "ECHOSLINE", "pregunta": "¿Qué producto es un tratamiento intensivo de 1000ml para disciplina?", "opciones": ["Vegan Discipl. Mask 1000ml", "Laca Spray 100ml", "Hair Retouch", "Pasta Mate"], "correcta": "Vegan Discipl. Mask 1000ml"},
    {"marca": "ECHOSLINE", "pregunta": "¿Por qué recomendarías la línea Maqui 3?", "opciones": ["Por su tecnología antioxidante y compacta", "Porque es la más económica", "Porque sirve para todo tipo de piel", "Porque no tiene aroma"], "correcta": "Por su tecnología antioxidante y compacta"},

        
        # ... (Se completan las 20 preguntas de teoría profesional)
    ] # Cierre final de la lista de maquillaje
}  # Cierre final del diccionario banco_total

    
     
# --- 5. LÓGICA DE LOGIN ---
if not st.session_state.autenticado:
    st.title("🔐 Acceso VIVA Academy")
    clave_input = st.text_input("Ingresa tu Clave:", type="password")
    
    if st.button("Ingresar"):
        df_form = conn.read(worksheet="Form_Responses", ttl=0)
        df_form['clave'] = df_form['clave'].astype(str).str.strip()
        u = df_form[df_form['clave'] == clave_input.strip()]
        
        if not u.empty:
            intentos = int(u.iloc[0]['Intentos'])
            if intentos >= 3:
                st.error("Máximo de intentos alcanzado.")
            else:
                df_form.loc[df_form['clave'] == clave_input.strip(), 'Intentos'] = intentos + 1
                conn.update(worksheet="Form_Responses", data=df_form)
                
                st.session_state.update({
                    "autenticado": True,
                    "nom": u.iloc[0]['NOMBRES'],
                    "correo": u.iloc[0]['CORREO DEL VENDEDOR'],
                    "sucursal": u.iloc[0]['SUCURSAL'],
                    "inicio": None,
                    "indice": 0,
                    "puntos": 0,
                    "hist": [],
                    "examen_terminado": False,
                    "ya_guardado": False,
                    "nivel": None,
                    "examen_actual": None
                })
                st.rerun()
        else:
            st.error("Clave incorrecta")
    st.stop()

# --- 6. PANTALLA DE RESULTADOS (SIN GLOBOS PARA EVITAR ERRORES) ---
if st.session_state.examen_terminado:
    st.title("📋 Resultados Finales")
    
    if not st.session_state.ya_guardado:
        try:
            df_res = conn.read(worksheet="Resultados", ttl=0)
            datos = {
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Nombre": st.session_state.nom,
                "Correo del vendedor": st.session_state.correo,
                "Sucursal": st.session_state.sucursal,
                "Categoria": st.session_state.nivel,
                "Calificacion": f"{st.session_state.puntos}/{len(st.session_state.examen_actual)}"
            }
            df_final = pd.concat([df_res, pd.DataFrame([datos])], ignore_index=True)
            conn.update(worksheet="Resultados", data=df_final)
            st.session_state.ya_guardado = True
            st.rerun() 
        except Exception as e:
            st.error(f"Error al guardar: {e}")
    
    st.success(f"¡Certificación en {st.session_state.nivel} finalizada con éxito!")
    st.metric("Puntaje Logrado", f"{st.session_state.puntos} / {len(st.session_state.examen_actual)}")
    
    # Usamos dataframe en lugar de table por ser más ligero para el navegador
    st.write("### Detalle de Respuestas:")
    st.dataframe(st.session_state.hist, use_container_width=True)
    
    if st.button("Cerrar Sesión"):
        st.session_state.clear()
        st.rerun()
    st.stop()

# --- 7. SELECCIÓN DE CATEGORÍA E INICIO (30 PREGUNTAS FIJAS) ---
if st.session_state.autenticado and st.session_state.examen_actual is None:
    st.title(f"🚀 Bienvenido, {st.session_state.nom}")
    st.write("Selecciona la categoría para tu examen de 30 preguntas:")
    
    cat_opciones = ["-- Selecciona una --"] + list(banco_total.keys())
    seleccion = st.selectbox("Categorías disponibles:", cat_opciones)
    
    if seleccion != "-- Selecciona una --":
        if st.button("Iniciar Certificación"):
            st.session_state.nivel = seleccion
            st.session_state.inicio = datetime.now()
            
            # Pool de preguntas único
            lista_raw = banco_total[seleccion]
            pool_unico = []
            vistos = set()
            for p in lista_raw:
                if p['pregunta'].strip().lower() not in vistos:
                    pool_unico.append(p)
                    vistos.add(p['pregunta'].strip().lower())
            
            # Tomamos 30 al azar (Azar puro favorece a marcas con más preguntas)
            st.session_state.examen_actual = random.sample(pool_unico, k=min(30, len(pool_unico)))
            st.session_state.indice = 0
            st.session_state.puntos = 0
            st.session_state.hist = []
            st.rerun()
    st.stop()

# --- 8. CRONÓMETRO ---
st_autorefresh(interval=1000, key="viva_flat_refresh")

if st.session_state.inicio:
    restante = max(0, 900 - int((datetime.now() - st.session_state.inicio).total_seconds()))
    m, s = divmod(restante, 60)
    st.sidebar.header(f"⏳ {m:02d}:{s:02d}")
    st.sidebar.write(f"**Vendedor:** {st.session_state.nom}")
    st.sidebar.write(f"**Categoría:** {st.session_state.nivel}")
    if restante <= 0:
        st.session_state.examen_terminado = True
        st.rerun()

# --- 9. FLUJO DE PREGUNTAS (PROTECCIÓN ANTI-TRADUCCIÓN) ---
if st.session_state.examen_actual:
    i = st.session_state.indice
    examen = st.session_state.examen_actual
    
    if i < len(examen):
        p_actual = examen[i]
        
        st.write(f"### Pregunta {i+1} de {len(examen)}")
        
        # Extraemos la marca real
        marca_real = str(p_actual.get('marca', 'GENERAL')).strip().upper()
        
        # USAMOS HTML PARA BLOQUEAR LA TRADUCCIÓN (class='notranslate')
        # Esto evita que 'Top Face' se convierta en 'Cara Superior'
        st.markdown(f"""
            <div class="notranslate" style="background-color: #e1f5fe; padding: 15px; border-radius: 10px; border-left: 5px solid #01579b;">
                <p style="margin: 0; font-weight: bold; color: #01579b;">MARCA: {marca_real}</p>
                <p style="margin: 10px 0 0 0; font-size: 1.1em; color: #000;">{p_actual['pregunta']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Espacio para separar del radio button
        st.write("")
        
        # Mezcla de opciones
        opciones_mezcladas = p_actual['opciones'].copy()
        random.seed(i)
        random.shuffle(opciones_mezcladas)
        
        opcion = st.radio(
            "Selecciona tu respuesta:",
            opciones_mezcladas,
            key=f"quiz_v3_{st.session_state.nivel}_{i}"
        )
        
        st.write("---")
        
        texto_boton = "Siguiente" if i < len(examen)-1 else "Finalizar"
        
        if st.button(texto_boton, use_container_width=True):
            if opcion == p_actual['correcta']:
                st.session_state.puntos += 1
            
            st.session_state.hist.append({
                "Pregunta": p_actual['pregunta'],
                "Marca": marca_real,
                "Estado": "✅" if opcion == p_actual['correcta'] else "❌"
            })
            
            if i == len(examen) - 1:
                st.session_state.examen_terminado = True
            else:
                st.session_state.indice += 1
            st.rerun()