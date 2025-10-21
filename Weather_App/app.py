import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import requests
from sklearn.linear_model import LinearRegression
import plotly.express as px

# Load API key
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    st.error("API_KEY not found in .env")
    st.stop()

# Title
st.title("🌤️ Weather Insight Dashboard")
st.write("Aayush Joshi's Real-time weather + 7-day trends + next-day forecast")

# Sidebar input
st.sidebar.header("City Search")
city_input = st.sidebar.text_input("Enter a city:")
city_list = st.sidebar.text_area("Or multiple cities (comma-separated):")

cities = []
if city_input:
    cities.append(city_input.strip())
if city_list:
    cities.extend([c.strip() for c in city_list.split(",") if c.strip()])

# CSV file
file_path = "data/weather_data.csv"
os.makedirs("data", exist_ok=True)

# Fetch weather function
def fetch_weather(city_name):
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        weather_dict = {
            "City": city_name,
            "Temperature (°C)": data["main"]["temp"],
            "Feels Like (°C)": data["main"]["feels_like"],
            "Humidity (%)": data["main"]["humidity"],
            "Pressure (hPa)": data["main"]["pressure"],
            "Weather": data["weather"][0]["main"],
            "Wind Speed (m/s)": data["wind"]["speed"],
            "Timestamp": timestamp
        }
        df_new = pd.DataFrame([weather_dict])
        if not os.path.exists(file_path):
            df_new.to_csv(file_path, index=False)
        else:
            df_new.to_csv(file_path, mode='a', index=False, header=False)
        return weather_dict
    except:
        return None

# Fetch button
if st.sidebar.button("Fetch Weather"):
    for city in cities:
        result = fetch_weather(city)
        if result:
            st.success(f"Weather fetched for {city}")

# Load CSV safely and keep only the latest entry per city
if os.path.exists(file_path):
    expected_cols = ["City", "Temperature (°C)", "Feels Like (°C)",
                     "Humidity (%)", "Pressure (hPa)", "Weather",
                     "Wind Speed (m/s)", "Timestamp"]
    df = pd.read_csv(file_path, names=expected_cols, header=0)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Keep only latest record per city
    df_latest = df.loc[df.groupby("City")["Timestamp"].idxmax()].reset_index(drop=True)

    st.write("### Latest Weather Records (Most Recent per City)")
    st.dataframe(df_latest)

    # City selector
    selected_city = st.selectbox("Select city to view 7-day trends", df["City"].unique())
    city_df = df[df["City"] == selected_city].sort_values("Timestamp")

    # Last 7 days
    last_7_days = city_df[city_df["Timestamp"] >= (datetime.now() - timedelta(days=7))]

    # Temperature trend line chart
    st.write(f"### Temperature & Feels Like - Last 7 Days ({selected_city})")
    st.line_chart(last_7_days.set_index("Timestamp")[["Temperature (°C)", "Feels Like (°C)"]])

    # Humidity trend bar chart
    st.write(f"### Humidity - Last 7 Days ({selected_city})")
    st.bar_chart(last_7_days.set_index("Timestamp")["Humidity (%)"])

    # Weather distribution donut chart using Plotly
    st.write(f"### Weather Distribution - Last 7 Days ({selected_city})")
    weather_counts = last_7_days["Weather"].value_counts().reset_index()
    weather_counts.columns = ["Weather", "Count"]
    fig = px.pie(weather_counts, names="Weather", values="Count",
                 color_discrete_sequence=px.colors.qualitative.Set3,
                 hole=0.4)  # Donut style
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)

    # Next-day temperature forecast (linear regression)
    st.write(f"### Next-Day Temperature Forecast - {selected_city}")
    if len(last_7_days) >= 2:
        last_7_days = last_7_days.reset_index()
        X = np.arange(len(last_7_days)).reshape(-1,1)
        y = last_7_days["Temperature (°C)"].values
        model = LinearRegression()
        model.fit(X, y)
        next_day_pred = model.predict(np.array([[len(last_7_days)]]))[0]
        st.metric("Predicted Temperature (°C) Tomorrow", f"{next_day_pred:.2f}°C")
    else:
        st.info("Not enough data for forecast. Fetch more data.")
