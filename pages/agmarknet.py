import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ------------- Agmarknet Scraper Logic -------------
def fetch_agmarknet_data(state, commodity, market):
    url = "https://agmarknet.gov.in/SearchCmmMkt.aspx"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)

        Select(driver.find_element(By.ID, 'ddlCommodity')).select_by_visible_text(commodity)
        Select(driver.find_element(By.ID, 'ddlState')).select_by_visible_text(state)

        past_date = datetime.now() - timedelta(days=7)
        driver.find_element(By.ID, "txtDate").clear()
        driver.find_element(By.ID, "txtDate").send_keys(past_date.strftime('%d-%b-%Y'))

        driver.find_element(By.ID, 'btnGo').click()
        time.sleep(2)

        Select(driver.find_element(By.ID, 'ddlMarket')).select_by_visible_text(market)
        driver.find_element(By.ID, 'btnGo').click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cphBody_GridPriceData')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        data_list = []
        for row in soup.find_all("tr"):
            data_list.append(row.text.replace("\n", "_").replace("  ", "").split("__"))

        json_list = []
        for i in data_list[4:-1]:
            if len(i) >= 11:
                entry = {
                    "S.No": i[1],
                    "City": i[2],
                    "Commodity": i[4],
                    "Min Price": i[7],
                    "Max Price": i[8],
                    "Model Price": i[9],
                    "Date": i[10]
                }
                if entry['City'].strip().lower() == market.strip().lower():
                    json_list.append(entry)

        return json_list

    except Exception as e:
        return str(e)
    finally:
        driver.quit()


# ------------------ Streamlit Page Logic ------------------ #
def show():
    st.title("📊 Agmarknet Market Prices")

    st.markdown("Get recent commodity price updates from the Indian Government’s Agmarknet Portal.")

    col1, col2, col3 = st.columns(3)
    with col1:
        state = st.text_input("Enter State", value="Maharashtra")
    with col2:
        commodity = st.text_input("Enter Commodity", value="Tomato")
    with col3:
        market = st.text_input("Enter Market", value="Pune")

    if st.button("📈 Fetch Crop Prices"):
        with st.spinner("Fetching data from Agmarknet..."):
            result = fetch_agmarknet_data(state, commodity, market)

            if isinstance(result, str):
                st.error(f"❌ Error: {result}")
            elif result:
                df = pd.DataFrame(result)
                st.success(f"✅ {len(df)} records fetched.")
                st.dataframe(df)

                if 'Date' in df.columns and 'Model Price' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                    df = df.dropna(subset=['Date'])
                    df = df.sort_values(by='Date')

                    st.markdown("#### 📊 Model Price Over Time")
                    st.line_chart(df.set_index('Date')['Model Price'])

                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download CSV", csv, f"{commodity}_prices.csv", "text/csv")
            else:
                st.warning("⚠️ No data found or invalid input.")
