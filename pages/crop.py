# pages/crop.py

import streamlit as st
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ---------------------- Load Crop Data ----------------------
@st.cache_data
def load_crop_data():
    file_path = os.path.join("Crop_recommendation.csv")
    if not os.path.exists(file_path):
        st.error("❌ 'Crop_recommendation.csv' not found in the 'data/' folder.")
        return pd.DataFrame()
    return pd.read_csv(file_path)


# ---------------------- Page Logic ----------------------
def show():
    st.title("🌾 Crop Recommendation System")

    crop_df = load_crop_data()

    if crop_df.empty:
        st.warning("⚠️ Could not load crop dataset.")
        return

    st.subheader("📋 Dataset Preview")
    st.dataframe(crop_df.head())

    # Prepare data
    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    target = 'label'
    X = crop_df[features]
    y = crop_df[target]

    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train_scaled, y_train)

    # Sidebar input
    st.sidebar.subheader("🌿 Enter Soil & Weather Parameters")
    user_input = [
        st.sidebar.number_input("Nitrogen (N)", 0),
        st.sidebar.number_input("Phosphorous (P)", 0),
        st.sidebar.number_input("Potassium (K)", 0),
        st.sidebar.number_input("Temperature (°C)", 0.0),
        st.sidebar.number_input("Humidity (%)", 0.0),
        st.sidebar.number_input("pH", 0.0),
        st.sidebar.number_input("Rainfall (mm)", 0.0)
    ]

    # Make prediction
    if st.sidebar.button("🌱 Get Crop Recommendation"):
        input_scaled = scaler.transform([user_input])
        prediction = model.predict(input_scaled)[0]
        st.sidebar.success(f"✅ Recommended Crop: **{prediction}**")
        st.success(f"📌 Based on your input, the most suitable crop is: **{prediction}**")
        st.session_state.predicted_crop = prediction
