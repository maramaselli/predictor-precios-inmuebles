<<<<<<< HEAD
# instalar gradio_client antes de procesar (pip istall gradio_client)

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
=======
# instalar gradio_client antes de procesar (pip istall gradio_client)

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
>>>>>>> 03d283f17710b30a873a51b2b504ebc7c6978069
print(result)