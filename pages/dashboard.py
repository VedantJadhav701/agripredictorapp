# pages/dashboard.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def show():
    st.header("📊 Dashboard Overview")
    st.markdown("Welcome to **AgriPredictor** — your smart farming assistant.")

    # Add a try-except for safety
    try:
        crop_df = pd.read_csv("Crop_recommendation.csv")
        fert_df = pd.read_csv("Fertilizer.csv")
    except FileNotFoundError:
        st.error("❌ Required data files not found.")
        return

    st.subheader("📁 Dataset Summary")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("📄 Crop Records", len(crop_df))
        st.dataframe(crop_df.head(), height=200)

    with col2:
        st.metric("🧪 Fertilizer Records", len(fert_df))
        st.dataframe(fert_df.head(), height=200)

    st.subheader("🌾 Crop Frequency Distribution")
    fig1, ax1 = plt.subplots()
    sns.barplot(y=crop_df['label'].value_counts().index,
                x=crop_df['label'].value_counts().values, ax=ax1, palette="viridis")
    st.pyplot(fig1)

    st.subheader("🧪 Average Fertilizer Nutrients (NPK)")
    fig2, ax2 = plt.subplots()
    fert_df[['Nitrogen', 'Phosphorous', 'Potassium']].mean().plot(kind='bar', ax=ax2,
        color=['#90EE90', '#ADD8E6', '#FFCCCB'])
    st.pyplot(fig2)

    st.info("💡 Use the sidebar to explore predictions, forecasts, and Agmarknet data.")
