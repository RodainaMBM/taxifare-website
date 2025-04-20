import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import pydeck as pdk

st.title("🚕 Taxi Fare Prediction App")

st.markdown("Predict the fare of a NYC cab ride by entering your trip details:")

date = st.date_input("Date", value=datetime.today())
time = st.time_input("Time", value=datetime.now().time())
pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.758896)
passenger_count = st.slider("Number of Passengers", 1, 8, 1)

pickup_datetime = f"{date} {time}"


params = {
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

if st.button("Predict Fare"):
    try:
        url = "https://taxifare.lewagon.ai/predict"
        response = requests.get(url, params=params)
        prediction = response.json().get("fare", None)

        if prediction is not None:
            st.success(f"💵 Estimated fare: ${prediction:.2f}")
        else:
            st.warning("No fare prediction returned.")
    except Exception as e:
        st.error(f"🚨 Error calling the API: {e}")


st.markdown("### 🗺️ Ride Map")
map_df = pd.DataFrame([
    {"lat": pickup_latitude, "lon": pickup_longitude, "label": "Pickup"},
    {"lat": dropoff_latitude, "lon": dropoff_longitude, "label": "Dropoff"}
])

st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=pickup_latitude,
        longitude=pickup_longitude,
        zoom=12,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=100,
        ),
        pdk.Layer(
            "TextLayer",
            data=map_df,
            get_position='[lon, lat]',
            get_text='label',
            get_size=16,
            get_color='[0, 0, 0]',
            get_angle=0,
            get_alignment_baseline="'bottom'"
        )
    ]
))
