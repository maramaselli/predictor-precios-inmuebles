from gradio_client import Client

# Si estás en local
client = Client("http://127.0.0.1:7860/")

# Si ya está desplegado en Hugging Face Spaces reemplazar por:
# client = Client(""https://Mara1989-predictor-precios-inmuebles.hf.space"")

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