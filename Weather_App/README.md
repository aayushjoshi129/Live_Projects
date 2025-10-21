# 🌤️ Weather Insight Dashboard

An interactive **Weather Dashboard** built with **Python**, **Streamlit**, **Pandas**, **NumPy**, and **Plotly**, showcasing my journey towards becoming a **Data Scientist**. This project fetches real-time weather data, stores it, visualizes 7-day trends, and predicts next-day temperature using **Linear Regression**.

---

## **Table of Contents**

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Technologies & Libraries](#technologies--libraries)  
4. [Setup & Installation](#setup--installation)  
5. [Usage](#usage)  
6. [Folder Structure](#folder-structure)  
7. [Screenshots](#screenshots)  
8. [Future Enhancements](#future-enhancements)  
9. [Portfolio Impact](#portfolio-impact)  

---

## **Project Overview**

This project is designed to demonstrate **data collection, storage, analysis, visualization, and predictive modeling** skills:

- Fetch **real-time weather** data from **OpenWeatherMap API**.  
- Store historical weather records in a CSV file.  
- Display **latest weather per city**.  
- Show **temperature and humidity trends** over the past 7 days.  
- Visualize **weather condition distribution** using a **donut chart**.  
- Predict **next-day temperature** using **Linear Regression**.  

This dashboard is **interactive**, **portfolio-ready**, and demonstrates **end-to-end Data Science workflow**.

---

## **Features**

- 🌍 **City search** (single or multiple cities)  
- 📊 **7-day temperature & humidity trends**  
- 🍩 **Weather condition distribution chart** (Plotly donut chart)  
- 🔮 **Next-day temperature forecast** using Linear Regression  
- 💾 **Automatic CSV storage** of all fetched data  
- ✅ **Latest record display** per city to avoid duplicates  

---

## **Technologies & Libraries**

- **Python**: Core language  
- **Streamlit**: Interactive dashboard creation  
- **Pandas**: Data handling and CSV management  
- **NumPy**: Numerical operations and array manipulations  
- **Requests**: Fetch data from API  
- **Plotly Express**: Interactive charts  
- **Scikit-learn**: Linear Regression model for forecasting  
- **python-dotenv**: Environment variable management  

---

## **Setup & Installation**

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/weather-insight-dashboard.git
cd weather-insight-dashboard
```

2. **Create a virtual environment:**

```
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

3. **Install dependencies:**

```
pip install -r requirements.txt

```

4. **Setup .env file:**

```
API_KEY=your_openweathermap_api_key
```

5. **Run the Streamlit app:**

```
streamlit run app.py
```

6. **Usage**

```
Open the sidebar and enter a city or multiple cities (comma-separated).

Click "Fetch Weather" to retrieve real-time weather data.

View latest weather records per city.

Select a city from the dropdown to view:

7-day temperature & humidity trends

Weather condition distribution donut chart

Next-day temperature forecast

The app automatically stores all fetched data in data/weather_data.csv for historical analysis.




weather-insight-dashboard/
│
├── app.py                  # Streamlit dashboard
├── fetch_weather.py        # Terminal-based weather fetch script
├── data/                   # Folder for CSV storage
│   └── weather_data.csv
├── .env                    # API key (not committed to GitHub)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

```