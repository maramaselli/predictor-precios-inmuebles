
# 🏡 Predictor de Precios Inmobiliarios

Esta aplicación permite estimar el precio de una propiedad en USD a partir de sus características principales (cantidad de ambientes, dormitorios, baños, superficie total, superficie cubierta, tipo de propiedad, localidad y zona).

La interfaz fue desarrollada con **Gradio** y el modelo fue entrenado previamente con datos históricos del mercado inmobiliario argentino.

## 🚀 Link al Space

👉 [Abrir la aplicación en Hugging Face Spaces](https://huggingface.co/spaces/Mara1989/predictor-precios-inmuebles)

## 🖼️ Captura de pantalla

![App en funcionamiento](captura.png)

## 🧠 Ejemplo de uso del endpoint

pip install gradio_client

from gradio_client import Client

from gradio_client import Client

client = Client("Mara1989/predictor-precios-inmuebles")
result = client.predict(
		rooms=3,
		bedrooms=1,
		bathrooms=1,
		surface_total=60,
		surface_covered=55,
		place_name="Abasto",
		property_type="Casa",
		state_name="Capital Federal",
		api_name="/predict_price"
)
print(result)