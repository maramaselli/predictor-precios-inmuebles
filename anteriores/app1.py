import gradio as gr
import pandas as pd
import pickle
import numpy as np

# === CARGA DE MODELO Y PREPROCESADORES ===
base = r"C:\Users\USER\Desktop\Escuela de Datos Vivos\model"

with open(f"{base}\\rf_robusto.pkl", "rb") as f:
    model = pickle.load(f)

with open(f"{base}\\place_name_freq.pkl", "rb") as f:
    place_name_freq = pickle.load(f)

with open(f"{base}\\property_ohe.pkl", "rb") as f:
    property_ohe = pickle.load(f)

with open(f"{base}\\state_ohe.pkl", "rb") as f:
    state_ohe = pickle.load(f)

with open(f"{base}\\feature_columns.pkl", "rb") as f:
    feature_columns = pickle.load(f)

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
place_name_options = list(place_name_freq.keys())
property_type_options = list(property_ohe.categories_[0])
state_name_options = list(state_ohe.categories_[0])

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏡 Estimador de Precio de Propiedades")

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

    predict_btn.click(predict_price,
                      inputs=[rooms, bedrooms, bathrooms, surface_total, surface_covered, place_name, property_type, state_name],
                      outputs=output)

if __name__ == "__main__":
    demo.launch(share=True)