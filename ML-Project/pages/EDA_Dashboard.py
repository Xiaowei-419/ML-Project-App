import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="EDA Dashboard", page_icon="📊", layout="wide")
st.title("📊 Exploratory Data Analysis Dashboard")

@st.cache_data
def load_data():
    # Reads your real processed CSV file directly from your root directory
    df = pd.read_csv("dating_data_final_processed.csv")
    return df

# Load the real dataset
df = load_data()

st.markdown("### 📋 Dataset Overview Sample")
st.dataframe(df.head(10), use_container_width=True)

# Metric layout blocks linked to your real CSV variables
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Total Dataset Records", f"{len(df):,}")

# Check if 'AppUsage' or original metrics exist to calculate averages dynamically
if 'AppUsage' in df.columns:
    col_m2.metric("Average App Usage (Scaled)", f"{df['AppUsage'].mean():.2f}")
else:
    col_m2.metric("Columns Logged", f"{len(df.columns)} Features")

if 'match_outcome' in df.columns:
    col_m3.metric("Most Frequent Outcome", df['match_outcome'].mode()[0])
else:
    col_m3.metric("Target Feature", "Outcome_encoded")

st.markdown("---")
st.markdown("### 📈 Visualizing Interactive Feature Variations")

# Dynamically populate select boxes with all available features except the target outcome column
numeric_features = [col for col in df.columns if col not in ['match_outcome', 'Outcome_encoded']]
feature_x = st.selectbox("Select X-Axis Feature:", numeric_features, index=0)
feature_y = st.selectbox("Select Y-Axis Feature:", numeric_features, index=min(1, len(numeric_features)-1))

# Determine the best coloring column available in your processed file
color_target = 'match_outcome' if 'match_outcome' in df.columns else 'Outcome_encoded'

fig = px.scatter(df, x=feature_x, y=feature_y, color=color_target, 
                 title=f"{feature_x} vs {feature_y} Segmented by Outcome",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig, use_container_width=True)

# Distribution plots
st.markdown("### 🗺️ Class Distribution Breakdown")
if color_target in df.columns:
    fig_pie = px.pie(df, names=color_target, title="Dating Trajectory Distributions", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("Target mapping classes not detected for pie distribution visualization.")