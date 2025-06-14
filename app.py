import streamlit as st
import requests
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="TaxiFare Predictor", page_icon="🚕", layout="centered")

st.title("Taxi Fare Estimator")
st.subheader("Predice el costo de tu viaje en New York en segundos")
st.markdown("Interactúa con los campos, envía tu solicitud y observa el mapa con tu ruta! 🗺️")

# Inputs
with st.form("fare_form"):
    col1, col2 = st.columns(2)

    with col1:
        pickup_date = st.date_input("Fecha de recogida", value=datetime.today())
        pickup_time = st.time_input("Hora de recogida", value=datetime.now().time())
        passenger_count = st.number_input("Número de pasajeros", min_value=1, max_value=8, value=1)

    with col2:
        pickup_longitude = st.number_input("Longitud recogida", value=-73.985428, format="%.6f")
        pickup_latitude = st.number_input("Latitud recogida", value=40.748817, format="%.6f")
        dropoff_longitude = st.number_input("Longitud destino", value=-73.985428, format="%.6f")
        dropoff_latitude = st.number_input("Latitud destino", value=40.748817, format="%.6f")

    submitted = st.form_submit_button("Predecir tarifa")

if submitted:
    pickup_datetime = f"{pickup_date} {pickup_time}"
    url = "https://taxifare.lewagon.ai/predict"

    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        fare = response.json().get("fare", "No disponible")
        st.success(f"Tarifa estimada: ${fare:.2f}")

        # Mapa interactivo
        st.markdown("### Vista del trayecto")
        map_data = pd.DataFrame({
            'lat': [pickup_latitude, dropoff_latitude],
            'lon': [pickup_longitude, dropoff_longitude]
        }, index=["Recogida", "Destino"])
        st.map(map_data)

    else:
        st.error("❌ Error al contactar la API. Verifica que esté en línea.")
