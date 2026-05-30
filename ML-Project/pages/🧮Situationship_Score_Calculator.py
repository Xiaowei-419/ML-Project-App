import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Predict Your Destiny", page_icon="🔮", layout="wide")

st.title("🔮 Situationship Score & Outcome Predictor")
st.markdown("""
Curious about your digital connection status? Provide your app interaction details below. 
Our systems will calculate your custom **Situationship Index Score** and run it through our Machine Learning engine 
to forecast your ultimate dating app destiny!
""")

st.markdown("---")

# --- STEP 1: USER BEHAVIOR CAPTURE FORM ---
st.markdown("### 📝 Profile & App Behavior Entry")

form_col1, form_col2, form_col3 = st.columns(3)

with form_col1:
    app_usage_time = st.number_input("Daily App Usage (Hours):", min_value=1, max_value=300, value=45)
    swipe_right_ratio = st.slider("Swipe Right Rate (%):", min_value=0, max_value=100, value=40) / 100.0
    message_sent = st.number_input("Messages Sent Daily:", min_value=0, max_value=500, value=25)

with form_col2:
    emoji_rate = st.slider("Emoji Usage Rate (%):", min_value=0, max_value=100, value=30) / 100.0
    bio_length = st.number_input("Bio Length:", min_value=0, max_value=500, value=150)
    profile_pics = st.number_input("Profile Pictures Uploaded:", min_value=1, max_value=10, value=4)

with form_col3:
    # Capturing input values to approximate Match Rates safely
    likes_received = st.number_input("Approx. Likes Received Weekly:", min_value=0, max_value=1000, value=50)
    matches_rec = st.number_input("Approx. Mutual Matches Weekly:", min_value=0, max_value=1000, value=10)
    
    # Ordinal Mapping Selectors aligned with your Kaggle script rules
    area_type = st.selectbox("Current Area Setting:", ["Urban", "Rural"])
    education_level = st.selectbox("Highest Education Level:", ["High School / Diploma", "Undergraduate Degree", "Postgraduate (Master's/PhD)"])

# Calculate intermediate inputs safely to feed into the index algorithm
match_rate = np.clip((matches_rec / (likes_received + 1)), 0.0, 1.0)
efficiency = np.clip((matches_rec / (app_usage_time + 0.1)), 0.0, 1.0)

# Apply Ordinal Encodings matching your project notebook rules
encoded_location = 1 if area_type == "Urban" else 0
encoded_edu = 1 if "High School" in education_level else (2 if "Undergraduate" in education_level else 3)

# --- STEP 2: RUN COMPUTATION ON BUTTON CLICK ---
if st.button("🔮 Calculate Scores & Predict Destiny", use_container_width=True):
    
    # 1. Compute Dynamic Innovation Layer Formula (0-100 score matching your code)
    # The project bounds scale elements via standard weights:
    situationship_score = 100 * (
        0.35 * (app_usage_time / 300.0) + 
        0.25 * swipe_right_ratio + 
        0.25 * (1.0 - match_rate) + 
        0.15 * (1.0 - efficiency)
    )
    situationship_score = float(np.clip(situationship_score, 0.0, 100.0))

    # 2. Mock Machine Learning Inference Engine 
    # (Simulates your trained Logistic Regression/Random Forest logic based on calculated scores)
    if situationship_score > 60:
        predicted_class = "Catfished 🕵️‍♂️"
        probability = [0.15, 0.15, 0.70]
        verdict_color = "red"
        advice = "⚠️ **High Alert:** Your score signals erratic behaviors or high interaction with inconsistent profiles. Verify your connections outside the app quickly!"
    elif situationship_score < 38:
        predicted_class = "Mutual Match 👩‍❤️‍👨"
        probability = [0.10, 0.75, 0.15]
        verdict_color = "green"
        advice = "🎉 **Excellent Status:** Your behavior pattern reflects balanced usage and healthy profile engagement. You're on standard pathing to real connections!"
    else:
        predicted_class = "Ghosted 👻"
        probability = [0.65, 0.20, 0.15]
        verdict_color = "orange"
        advice = "💤 **Cautious Status:** High text-sending rates vs. low mutual return indicators point directly towards communication fading patterns."

    st.markdown("---")
    st.markdown("### 📊 Interactive Visual Summary Dashboard")

    # Layout for KPIs and visualizations
    dash_col1, dash_col2 = st.columns([1, 1.2])

    with dash_col1:
        # Visual Meter Gauge using Plotly
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = situationship_score,
            title = {'text': "Calculated Situationship Risk Index"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#2c3e50"},
                'steps': [
                    {'range': [0, 38], 'color': "#2ecc71"},   # Safe / Mutual Match zone
                    {'range': [38, 60], 'color': "#f1c40f"},  # Alert / Ghosted zone
                    {'range': [60, 100], 'color': "#e74c3c"}  # High Risk / Catfish zone
                ]
            }
        ))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Highlight Results Display Panel
        st.markdown(f"#### Predicted Destiny: :{verdict_color}[{predicted_class}]")
        st.info(advice)

    with dash_col2:
        # Probabilities Bar Chart using Plotly
        st.markdown("#### Engine Target Confidence Distribution")
        
        prob_df = pd.DataFrame({
            'Dating Trajectory': ['Ghosted 👻', 'Mutual Match 👩‍❤️‍👨', 'Catfished 🕵️‍♂️'],
            'Model Confidence (%)': [p * 100 for p in probability]
        })
        
        fig_bar = px.bar(
            prob_df, 
            x='Model Confidence (%)', 
            y='Dating Trajectory', 
            orientation='h',
            color='Dating Trajectory',
            color_discrete_map={'Mutual Match 👩‍❤️‍👨': '#2ecc71', 'Ghosted 👻': '#f1c40f', 'Catfished 🕵️‍♂️': '#e74c3c'},
            text=prob_df['Model Confidence (%)'].apply(lambda x: f"{x:.1f}%")
        )
        fig_bar.update_layout(height=320, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_bar, use_container_width=True)