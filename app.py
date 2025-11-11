import gradio as gr
import pandas as pd
import pickle
import numpy as np

# === CARGA DE MODELO Y PREPROCESADORES ===

with open("rf_robusto.pkl", "rb") as f:
    model = pickle.load(f)

with open("place_name_freq.pkl", "rb") as f:
    place_name_freq = pickle.load(f)

with open("property_ohe.pkl", "rb") as f:
    property_ohe = pickle.load(f)

with open("state_ohe.pkl", "rb") as f:
    state_ohe = pickle.load(f)

with open("feature_columns.pkl", "rb") as f:
    feature_columns = pickle.load(f)

# === MAPEOS (EDITAR CON TUS DATOS REALES) ===
localidad_a_zona = {
    "Colegiales": "Capital Federal",
    "Almagro": "Capital Federal",
    "Villa Urquiza": "Capital Federal",
    "Boedo": "Capital Federal",
    "San Telmo": "Capital Federal",
    "Barrio Norte": "Capital Federal",
    "Villa Devoto": "Capital Federal",
    "Palermo": "Capital Federal",
    "Monserrat": "Capital Federal",
    "Caballito": "Capital Federal",
    "Villa Ortuzar": "Capital Federal",
    "Villa Crespo": "Capital Federal",
    "Once": "Capital Federal",
    "Saavedra": "Capital Federal",
    "La Plata": "Bs.As. G.B.A. Zona Sur",
    "Recoleta": "Capital Federal",
    "Villa General Mitre": "Capital Federal",
    "Villa del Parque": "Capital Federal",
    "Belgrano": "Capital Federal",
    "Mataderos": "Capital Federal",
    "Balvanera": "Capital Federal",
    "Floresta": "Capital Federal",
    "Coghlan": "Capital Federal",
    "Flores": "Capital Federal",
    "Velez Sarsfield": "Capital Federal",
    "Parque Chacabuco": "Capital Federal",
    "Nuñez": "Capital Federal",
    "Las Cañitas": "Capital Federal",
    "Villa Riachuelo": "Capital Federal",
    "Paternal": "Capital Federal",
    "Congreso": "Capital Federal",
    "Parque Centenario": "Capital Federal",
    "Constitución": "Capital Federal",
    "Pompeya": "Capital Federal",
    "San Cristobal": "Capital Federal",
    "Villa Real": "Capital Federal",
    "Parque Patricios": "Capital Federal",
    "San Nicolás": "Capital Federal",
    "Boca": "Capital Federal",
    "Versalles": "Capital Federal",
    "Villa Luro": "Capital Federal",
    "Chacarita": "Capital Federal",
    "Retiro": "Capital Federal",
    "Barracas": "Capital Federal",
    "Monte Castro": "Capital Federal",
    "Villa Pueyrredón": "Capital Federal",
    "Parque Avellaneda": "Capital Federal",
    "Liniers": "Capital Federal",
    "Villa Lugano": "Capital Federal",
    "Abasto": "Capital Federal",
    "Puerto Madero": "Capital Federal",
    "Tribunales": "Capital Federal",
    "Centro / Microcentro": "Capital Federal",
    "Villa Santa Rita": "Capital Federal",
    "Agronomía": "Capital Federal",
    "Parque Chas": "Capital Federal",
    "Catalinas": "Capital Federal",
    "Tigre": "Bs.As. G.B.A. Zona Norte",
    "Lanús": "Bs.As. G.B.A. Zona Sur",
    "Pilar": "Bs.As. G.B.A. Zona Norte",
    "Avellaneda": "Bs.As. G.B.A. Zona Sur",
    "La Matanza": "Bs.As. G.B.A. Zona Oeste",
    "San Isidro": "Bs.As. G.B.A. Zona Norte",
    "Vicente López": "Bs.As. G.B.A. Zona Norte",
    "Malvinas Argentinas": "Bs.As. G.B.A. Zona Norte",
    "General San Martín": "Bs.As. G.B.A. Zona Norte",
    "Ituzaingó": "Bs.As. G.B.A. Zona Oeste",
    "Berazategui": "Bs.As. G.B.A. Zona Sur",
    "Morón": "Bs.As. G.B.A. Zona Oeste",
    "Lomas de Zamora": "Bs.As. G.B.A. Zona Sur",
    "Tres de Febrero": "Bs.As. G.B.A. Zona Oeste",
    "Ezeiza": "Bs.As. G.B.A. Zona Sur",
    "San Fernando": "Bs.As. G.B.A. Zona Norte",
    "Merlo": "Bs.As. G.B.A. Zona Oeste",
    "Moreno": "Bs.As. G.B.A. Zona Oeste",
    "San Miguel": "Bs.As. G.B.A. Zona Norte",
    "Esteban Echeverría": "Bs.As. G.B.A. Zona Sur",
    "José C Paz": "Bs.As. G.B.A. Zona Norte",
    "Escobar": "Bs.As. G.B.A. Zona Norte",
    "Almirante Brown": "Bs.As. G.B.A. Zona Sur",
    "Quilmes": "Bs.As. G.B.A. Zona Sur",
    "Hurlingham": "Bs.As. G.B.A. Zona Oeste",
    "Villa Soldati": "Capital Federal",
    "San Vicente": "Bs.As. G.B.A. Zona Sur",
    "Presidente Perón": "Bs.As. G.B.A. Zona Sur",
    "Marcos Paz": "Bs.As. G.B.A. Zona Oeste",
    "Florencio Varela": "Bs.As. G.B.A. Zona Sur",
    "General Rodríguez": "Bs.As. G.B.A. Zona Oeste"
}

# === FUNCIÓN DE PREPROCESAMIENTO ===
def preprocess_new_data(new_data):
    df = pd.DataFrame([new_data])

    processed = {}

    # Variables numéricas
    for col in ['rooms', 'bedrooms', 'bathrooms', 'surface_total', 'surface_covered']:
        processed[col] = df[col].values[0]

    # Frequency encoding
    processed['place_name_freq'] = place_name_freq.get(df['place_name'].values[0], 0.0)

    # OHE Property Type
    prop_ohe = property_ohe.transform(df[['property_type']])
    prop_cols = [f"property_{cat}" for cat in property_ohe.categories_[0][1:]]
    for i, col in enumerate(prop_cols):
        processed[col] = prop_ohe[0][i]

    # OHE State
    state_ohe_data = state_ohe.transform(df[['state_name']])
    state_cols = [f"state_{cat}" for cat in state_ohe.categories_[0][1:]]
    for i, col in enumerate(state_cols):
        processed[col] = state_ohe_data[0][i]

    final = [processed[col] for col in feature_columns]
    return np.array(final).reshape(1, -1)

# === FUNCIÓN DE PREDICCIÓN ===
def predict_price(rooms, bedrooms, bathrooms, surface_total, surface_covered, place_name, property_type, state_name):

    # *** Validación 0: superficies mayores a cero ***
    if surface_total <= 0 or surface_covered <= 0:
        return "⚠️ La superficie total y la superficie cubierta deben ser mayores a 0."

    # *** Validación 1: tamaños coherentes ***
    if surface_total < surface_covered:
        return "⚠️ La superficie total no puede ser menor que la superficie cubierta."

    # *** Validación 2: zona coherente con localidad ***
    if place_name in localidad_a_zona:
        if localidad_a_zona[place_name] != state_name:
            return f"⚠️ La localidad {place_name} pertenece a la zona '{localidad_a_zona[place_name]}'. Por favor seleccioná la zona correcta."

    row = {
        'rooms': rooms,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'surface_total': surface_total,
        'surface_covered': surface_covered,
        'place_name': place_name,
        'property_type': property_type,
        'state_name': state_name
    }

    X = preprocess_new_data(row)
    pred = model.predict(X)[0]
    return f"💰 **USD {pred:,.0f}**"

# === UI GRADIO ===
place_name_options = sorted(list(place_name_freq.keys()))   # <-- ORDENADO ALFABÉTICO
property_type_options = list(property_ohe.categories_[0])
state_name_options = list(state_ohe.categories_[0])

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏡 Estimador de Precio de Propiedades")
    gr.Markdown("**Predice el valor de Propiedades en Venta de Capital y GBA usando Machine Learning**  \n_Basado en información recopilada durante 2019 y 2020 por Properati_")

    # ===================== CONTROLES =====================
    with gr.Row():
        with gr.Column():
            rooms = gr.Slider(1, 10, value=3, step=1, label="Ambientes")
            bedrooms = gr.Slider(0, 6, value=1, step=1, label="Dormitorios")
            bathrooms = gr.Slider(1, 5, value=1, step=1, label="Baños")
            surface_total = gr.Number(label="Superficie Total (m²)", value=60)
            surface_covered = gr.Number(label="Superficie Cubierta (m²)", value=55)

        with gr.Column():
            place_name = gr.Dropdown(place_name_options, label="Localidad")
            property_type = gr.Dropdown(property_type_options, label="Tipo de Propiedad")
            state_name = gr.Dropdown(state_name_options, label="Zona")

            predict_btn = gr.Button("🔮 Predecir Precio", variant="primary")
            output = gr.Label(label="Resultado")


    predict_btn.click(
        predict_price,
        inputs=[rooms, bedrooms, bathrooms, surface_total, surface_covered, place_name, property_type, state_name],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(share=True)