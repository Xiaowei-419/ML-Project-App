import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Model Evaluation", page_icon="🤖")
st.title("🤖 Model Comparison & Benchmark Analytics")

st.markdown("""
Below are the consolidated evaluation metrics obtained during our stratified Cross-Validation testing routines.
""")

# Replicating your classification data metrics frame 
@st.cache_data
def get_model_metrics():
    data = {
        "Classifier Engine": ["Random Forest", "Gradient Boosting", "Logistic Regression", "Support Vector Classifier"],
        "Mean Accuracy": [0.8942, 0.9125, 0.7654, 0.8210],
        "Standard Deviation": [0.012, 0.009, 0.034, 0.018]
    }
    return pd.DataFrame(data)

df_metrics = get_model_metrics()

# Display Data Table
st.dataframe(df_metrics.style.highlight_max(axis=0, subset=['Mean Accuracy']), use_container_width=True)

# Interactive Bar Plot
st.markdown("### 📊 Accuracy Benchmarks Comparison")
fig_compare = px.bar(
    df_metrics, 
    x="Classifier Engine", 
    y="Mean Accuracy", 
    error_y="Standard Deviation",
    color="Classifier Engine",
    title="Model Accuracy Performance Ranges (with Error Bounds)"
)
st.plotly_chart(fig_compare, use_container_width=True)

st.info("🏆 **Conclusion:** Gradient Boosting demonstrated the highest testing accuracy stability across 5-fold stratification splits.")