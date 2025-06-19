import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, log_loss
import tracemalloc
import time

@st.cache_data
def load_fertilizer_data():
    return pd.read_csv("Fertilizer.csv")

def show():
    df = load_fertilizer_data()

    st.header("🧪 Fertilizer Recommendation")
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    if st.checkbox("📈 Show Fertilizer Data Visualizations"):
        st.subheader("Correlation Heatmap")
        fig3 = plt.figure(figsize=(8, 5))
        sns.heatmap(df.drop('Fertilizer Name', axis=1).corr(), annot=True, cmap='coolwarm')
        st.pyplot(fig3)

    # Prepare data
    label_encoder = LabelEncoder()
    df['Fertilizer Name'] = label_encoder.fit_transform(df['Fertilizer Name'])

    X = df[['Nitrogen', 'Potassium', 'Phosphorous']]
    y = df['Fertilizer Name']

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    def train_model(model):
        tracemalloc.start()
        start = time.time()
        model.fit(X_train_scaled, y_train)
        end = time.time()
        memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        y_pred = model.predict(X_test_scaled)
        probs = model.predict_proba(X_test_scaled)
        return {
            'model': model,
            'accuracy': accuracy_score(y_test, y_pred),
            'report': classification_report(y_test, y_pred, target_names=label_encoder.classes_),
            'conf_matrix': confusion_matrix(y_test, y_pred),
            'log_loss': log_loss(y_test, probs),
            'time': end - start,
            'memory': memory[1] / 1e6
        }

    if st.button("🚀 Train Fertilizer Model"):
        model_result = train_model(RandomForestClassifier())
        st.session_state.fert_model = model_result['model']
        st.code(model_result['report'])
        st.metric("Accuracy", f"{model_result['accuracy']*100:.2f}%")
        st.metric("Training Time", f"{model_result['time']:.2f}s")
        st.metric("Peak Memory Usage", f"{model_result['memory']:.2f} MB")

    st.sidebar.subheader("🔍 Predict Fertilizer")
    n = st.sidebar.number_input("Nitrogen", 0)
    p = st.sidebar.number_input("Phosphorous", 0)
    k = st.sidebar.number_input("Potassium", 0)

    if st.sidebar.button("Get Fertilizer Recommendation"):
        if "fert_model" not in st.session_state:
            st.sidebar.warning("⚠️ Please train the model first.")
        else:
            input_scaled = scaler.transform([[n, k, p]])
            pred = st.session_state.fert_model.predict(input_scaled)
            st.sidebar.success(f"✅ Recommended Fertilizer: **{label_encoder.inverse_transform(pred)[0]}**")
