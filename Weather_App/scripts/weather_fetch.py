import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found in .env")

# Ask user for city input
city = input("Enter city name: ").strip()

# Fetch weather from OpenWeatherMap
URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

try:
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()

    # Format timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    weather_dict = {
        "City": city,
        "Temperature (°C)": data["main"]["temp"],
        "Feels Like (°C)": data["main"]["feels_like"],
        "Humidity (%)": data["main"]["humidity"],
        "Pressure (hPa)": data["main"]["pressure"],
        "Weather": data["weather"][0]["main"],
        "Wind Speed (m/s)": data["wind"]["speed"],
        "Timestamp": timestamp
    }

    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)
    file_path = "data/weather_data.csv"

    # Convert to DataFrame
    df_new = pd.DataFrame([weather_dict])

    # Write CSV safely
    if not os.path.exists(file_path):
        df_new.to_csv(file_path, index=False)  # write headers
    else:
        df_new.to_csv(file_path, mode='a', index=False, header=False)  # append without headers

    print("\n✅ Weather info fetched successfully!")
    print(weather_dict)

except requests.exceptions.HTTPError as err:
    print(f"❌ HTTP Error: {err}")
except Exception as e:
    print(f"❌ Error: {e}")
