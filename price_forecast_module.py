# price_forecast_module.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import streamlit as st

def run_yearly_forecast():
    st.subheader("📅 Yearly Price Forecast")
    df = pd.read_csv("DatasetSIH1647.csv")
    df.set_index('Commodities', inplace=True)
    df = df.T
    df.index = pd.date_range(start='2014', periods=len(df), freq='YE')
    df = df.ffill()
    commodities = df.columns.tolist()

    selected = st.selectbox("Select a Commodity (Yearly)", commodities, key="yearly_select")
    if st.button("Forecast Yearly"):
        data = df[selected]
        model = SARIMAX(data, order=(1, 1, 1))  # ✅ FIXED: Removed seasonal_order
        result = model.fit(disp=False)
        forecast = result.get_forecast(steps=5)
        predicted = forecast.predicted_mean

        years = pd.date_range(start='2025', periods=5, freq='YE')
        st.line_chart(pd.DataFrame({f"{selected} Forecast": predicted}, index=years))
        st.write(pd.DataFrame({'Year': years, 'Forecast Price': predicted.values}))
        rmse = np.sqrt(((data - result.fittedvalues) ** 2).mean())
        st.success(f"Training RMSE: {rmse:.2f}")

def run_monthly_forecast():
    st.subheader("📆 Monthly Price Forecast")
    df = pd.read_csv("datamain.csv")
    df.set_index('Commodities', inplace=True)
    df = df.T
    df.index = pd.date_range(start='2014-01', periods=len(df), freq='M')
    df = df.ffill()
    commodities = df.columns.tolist()

    selected = st.selectbox("Select a Commodity (Monthly)", commodities, key="monthly_select")
    if st.button("Forecast Monthly"):
        data = df[selected]
        model = SARIMAX(data, order=(1, 1, 1))  # ✅ fixed: removed seasonal_order
        result = model.fit(disp=False)
        forecast = result.get_forecast(steps=12)
        predicted = forecast.predicted_mean

        months = pd.date_range(start='2025-01', periods=12, freq='M')
        st.line_chart(pd.DataFrame({f"{selected} Forecast": predicted}, index=months))
        st.write(pd.DataFrame({'Month': months, 'Forecast Price': predicted.values}))
        rmse = np.sqrt(((data - result.fittedvalues) ** 2).mean())
        st.success(f"Training RMSE: {rmse:.2f}")
