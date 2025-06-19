import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pages.forecast import get_weather_forecast

def show():
    st.title("📅 Crop Season & Income Estimator")

    @st.cache_data
    def load_production_data():
        return pd.read_csv("produce.csv")

    @st.cache_data
    def load_region_data():
        path = os.path.join("crop_production.csv")
        df = pd.read_csv(path)
        df = df.dropna(subset=["Production"])
        df = df[df["Production"] > 0]
        df = df.rename(columns={"State_Name": "State", "Crop": "Crop", "Season": "Season", "Production": "Production"})
        avg_income = df.groupby(["State", "Crop", "Season"])["Production"].mean().reset_index()
        avg_income["Income (INR)"] = avg_income["Production"] * 15000
        return avg_income

    STATE_COORDS = {
    "Andhra Pradesh": (15.9129, 79.7400),
    "Arunachal Pradesh": (28.2180, 94.7278),
    "Assam": (26.2006, 92.9376),
    "Bihar": (25.0961, 85.3131),
    "Chhattisgarh": (21.2787, 81.8661),
    "Goa": (15.2993, 74.1240),
    "Gujarat": (22.2587, 71.1924),
    "Haryana": (29.0588, 76.0856),
    "Himachal Pradesh": (31.1048, 77.1734),
    "Jharkhand": (23.6102, 85.2799),
    "Karnataka": (15.3173, 75.7139),
    "Kerala": (10.8505, 76.2711),
    "Madhya Pradesh": (22.9734, 78.6569),
    "Maharashtra": (19.7515, 75.7139),
    "Manipur": (24.6637, 93.9063),
    "Meghalaya": (25.4670, 91.3662),
    "Mizoram": (23.1645, 92.9376),
    "Nagaland": (26.1584, 94.5624),
    "Odisha": (20.9517, 85.0985),
    "Punjab": (31.1471, 75.3412),
    "Rajasthan": (27.0238, 74.2179),
    "Sikkim": (27.5330, 88.5122),
    "Tamil Nadu": (11.1271, 78.6569),
    "Telangana": (18.1124, 79.0193),
    "Tripura": (23.9408, 91.9882),
    "Uttar Pradesh": (26.8467, 80.9462),
    "Uttarakhand": (30.0668, 79.0193),
    "West Bengal": (22.9868, 87.8550),
    # Optional: Union Territories
    "Delhi": (28.7041, 77.1025),
    "Puducherry": (11.9416, 79.8083),
    "Jammu and Kashmir": (33.7782, 76.5762),
    "Ladakh": (34.1526, 77.5770),
    "Chandigarh": (30.7333, 76.7794),
    "Andaman and Nicobar Islands": (11.7401, 92.6586),
    "Dadra and Nagar Haveli and Daman and Diu": (20.3974, 72.8328),
    "Lakshadweep": (10.5667, 72.6417)
}


    prod_df = load_production_data()
    region_df = load_region_data()
    crop_list = prod_df['Particulars'].dropna().unique()

    default_crop = crop_list[0]
    if 'predicted_crop' in st.session_state:
        match = next((c for c in crop_list if st.session_state.predicted_crop.lower() in c.lower()), default_crop)
        default_crop = match

    crop_name = st.selectbox("🌾 Select a Crop", crop_list, index=list(crop_list).index(default_crop))
    crop_data = prod_df[prod_df["Particulars"] == crop_name]

    lower_name = crop_name.lower()
    if "kharif" in lower_name:
        season = "Kharif (Monsoon)"
    elif "rabi" in lower_name:
        season = "Rabi (Winter)"
    elif "whole year" in lower_name:
        season = "All Year"
    else:
        season = "Unknown"

    st.markdown(f"**🌤 Best Season to Plant**: `{season}`")

    crop_years = crop_data.iloc[:, 2:].T
    crop_years.columns = [crop_name]
    crop_years.index = crop_years.index.str.extract(r'(\d{4})')[0]
    crop_years = crop_years.dropna()

    # Convert all columns to numeric, coercing errors to NaN to avoid mixed types
    crop_years = crop_years.apply(pd.to_numeric, errors='coerce')

    st.line_chart(crop_years)

    st.markdown("#### 💰 Estimated Income")
    est_price = st.number_input("Enter estimated price per ton (INR)", min_value=1000, value=15000, step=500)

    crop_yields = pd.to_numeric(crop_years[crop_name], errors='coerce')
    valid_yields = crop_yields.dropna()

    if not valid_yields.empty:
        avg_yield = valid_yields.mean()
        income = avg_yield * est_price
        st.success(f"📦 Average Yield: {avg_yield:.2f} million tons")
        st.success(f"💸 Estimated Income: ₹{income:.2f} million")
    else:
        st.warning("⚠️ Yield data not available for this crop.")

    st.markdown("#### 🗌 Region-Specific Income & Weather")
    selected_state = st.selectbox("📍 Select State", sorted(region_df['State'].unique()))

    matched_row = region_df[
        (region_df['State'] == selected_state) &
        (region_df['Crop'].str.lower() == crop_name.lower())
    ]

    if not matched_row.empty:
        region_season = matched_row['Season'].values[0]
        region_income = matched_row['Income (INR)'].values[0]
        st.info(f"🌦 Season in {selected_state}: `{region_season}`\n💰 Avg Income: ₹{region_income:,.0f}")

    AGRO_API_KEY = "24f4184850c2b27a374e9d0e07c0b3db"

    if selected_state in STATE_COORDS:
        lat, lon = STATE_COORDS[selected_state]
        forecast_df = get_weather_forecast(lat, lon, AGRO_API_KEY)
        if forecast_df is not None and not isinstance(forecast_df, list):
            st.markdown("#### ⛅ 7-Day Weather Forecast")
            st.dataframe(forecast_df, use_container_width=True)
        else:
            st.error("❌ Could not retrieve weather forecast.")
    else:
        st.warning("⚠️ Weather data not available for this state.")
