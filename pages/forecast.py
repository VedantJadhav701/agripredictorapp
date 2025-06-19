import streamlit as st
import pandas as pd
import datetime
import requests
from price_forecast_module import run_yearly_forecast, run_monthly_forecast

# ------------------ Weather Forecast Utility ------------------ #
def get_weather_forecast(lat, lon, api_key):
    try:
        url = f"https://api.agromonitoring.com/agro/1.0/weather/forecast?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Debug: log full API response for diagnosis
        # st.write(f"DEBUG: Weather API response for lat={lat}, lon={lon}: {data}")

        # Check for error message in response
        if isinstance(data, dict) and data.get('cod') != '200':
            st.error(f"❌ Weather API error: {data.get('message', 'Unknown error')}")
            return None

        # Handle case where data is a list of forecast entries
        if isinstance(data, list):
            forecast_data = data[:7]
        elif isinstance(data, dict) and 'list' in data:
            forecast_data = data['list'][:7]
        else:
            # Unexpected data format
            return None

        forecast = []
        for item in forecast_data:  # Iterate over forecast entries
            # Use 'dt_txt' if available for date string, else fallback to 'dt' timestamp
            if 'dt_txt' in item:
                date = item['dt_txt'].split(' ')[0]
            else:
                date = datetime.datetime.utcfromtimestamp(item['dt']).strftime('%Y-%m-%d')
            temp_c = round(item['main']['temp'] - 273.15, 2)
            desc = item['weather'][0]['description'].title()
            humidity = item['main']['humidity']
            wind = item['wind']['speed']
            forecast.append({
                "Date": date,
                "Temperature (°C)": temp_c,
                "Weather": desc,
                "Humidity (%)": humidity,
                "Wind Speed (m/s)": wind
            })

        return pd.DataFrame(forecast)

    except Exception as e:
        st.error(f"❌ Failed to fetch weather data: {e}")
        return None


# ------------------ Forecast Page ------------------ #
def show():
    st.header("📈 Commodity Price Forecast")
    st.markdown("Use this tool to forecast market prices using historical data.")

    forecast_type = st.radio("📊 Select Forecast Type", ["Yearly Forecast", "Monthly Forecast"])

    if forecast_type == "Yearly Forecast":
        run_yearly_forecast()
    else:
        run_monthly_forecast()
