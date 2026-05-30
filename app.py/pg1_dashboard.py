import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="EDA Dashboard", page_icon="📊", layout="wide")
st.title("📊 Exploratory Data Analysis Dashboard")

# Synthetic data framework for display purposes if real file is large/missing
@st.cache_data
def load_data():
    # Replace this with your actual uploaded data loading path: pd.read_csv("your_cleaned_data.csv")
    import numpy as np
    np.random.seed(42)
    n = 300
    df = pd.DataFrame({
        'App Usage (hours/day)': np.random.uniform(0.5, 6.0, n),
        'Swipe Ratio': np.random.uniform(0.1, 0.95, n),
        'Messages Sent/Day': np.random.randint(5, 120, n),
        'Ghosted Rate': np.random.uniform(0.0, 1.0, n),
        'Outcome': np.random.choice(['Mutual Match', 'Ghosted', 'Catfished'], n, p=[0.5, 0.3, 0.2])
    })
    return df

df = load_data()

st.markdown("### 📋 Dataset Overview Sample")
st.dataframe(df.head(10), use_container_width=True)

# Metric layout blocks
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Total Records Mocked", len(df))
col_m2.metric("Average App Usage", f"{df['App Usage (hours/day)'].mean():.2f} hrs/day")
col_m3.metric("Most Frequent Outcome", df['Outcome'].mode()[0])

st.markdown("---")
st.markdown("### 📈 Visualizing Interactive Feature Variations")

# Toggle Plotting Dimensions
feature_x = st.selectbox("Select X-Axis Feature:", df.columns[:-1])
feature_y = st.selectbox("Select Y-Axis Feature:", df.columns[:-1], index=1)

fig = px.scatter(df, x=feature_x, y=feature_y, color='Outcome', 
                 title=f"{feature_x} vs {feature_y} Segmented by Outcome",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig, use_container_width=True)

# Distribution plots
st.markdown("### 🗺️ Class Distribution Breakdown")
fig_pie = px.pie(df, names='Outcome', title="Dating Trajectory Distributions", hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)