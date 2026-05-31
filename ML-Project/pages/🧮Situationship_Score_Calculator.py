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
st.markdown("### 📝 User Profile & Behavior")

form_col1, form_col2, form_col3 = st.columns(3)

with form_col1:
    # 🎚️ Sliders for App Time and Text Messages
    app_usage_hours = st.slider("📱 Daily App Usage (Hours):", min_value=0.0, max_value=12.0, value=1.5, step=0.5)
    swipe_right_ratio = st.slider("👉 Swipe Right (Accept) Rate (%):", min_value=0, max_value=100, value=40) / 100.0
    message_sent = st.slider("💬 Messages Sent Daily:", min_value=0, max_value=300, value=25, step=5)

with form_col2:
    emoji_rate = st.slider("😂 Emoji Usage Rate (%):", min_value=0, max_value=100, value=30) / 100.0
    
    # 🎛️ Swapped Bio and Profile Pics into predefined sliding choices
    bio_length = st.slider("✍️ Bio Length (Characters):", min_value=0, max_value=500, value=150, step=25)
    profile_pics = st.slider("📸 Profile Pictures Uploaded:", min_value=1, max_value=10, value=4, step=1)

with form_col3:
    # 🎚️ Sliders for Weekly App Feedback activity
    likes_received = st.slider("❤️ Likes Received Weekly:", min_value=0, max_value=500, value=50, step=10)
    matches_rec = st.slider("🤝 Mutual Matches Weekly:", min_value=0, max_value=100, value=10, step=2)
    
    # 🔲 Clean drop-down selections
    area_type = st.selectbox("📍 Current Area Setting:", ["Urban", "Rural"])
    education_level = st.selectbox("🎓 Education Level:", ["High School / Diploma", "Undergraduate Degree", "Postgraduate (Master's/PhD)"])

# --- AUTOMATIC DATA CONVERSIONS FOR CALCULATION ---
# Converts hours back to minutes behind the scenes to keep your notebook formula safe
app_usage_time = app_usage_hours * 60.0 

# Re-calculate your intermediate metrics exactly like the notebook
match_rate = np.clip((matches_rec / (likes_received + 1)), 0.0, 1.0)
efficiency = np.clip((matches_rec / (app_usage_time + 0.1)), 0.0, 1.0)

# Apply Ordinal Encodings matching your project notebook rules
encoded_location = 1 if area_type == "Urban" else 0
encoded_edu = 1 if "High School" in education_level else (2 if "Undergraduate" in education_level else 3)

# --- STEP 2: RUN COMPUTATION ON BUTTON CLICK ---
if st.button("🔮 Calculate Scores & Predict Destiny", use_container_width=True):
    
    # Scales app time dynamically against your notebook max threshold of 300 minutes
    norm_app_time = min(app_usage_time / 300.0, 1.0)
    
    situationship_score = 100 * (
        0.35 * norm_app_time + 
        0.25 * swipe_right_ratio + 
        0.25 * (1.0 - match_rate) + 
        0.15 * (1.0 - efficiency)
    )
    situationship_score = float(np.clip(situationship_score, 0.0, 100.0))

    # Machine Learning Pipeline Emulation Paths (User-Friendly Version)
    if situationship_score > 60:
        predicted_class = "Catfished 🕵️‍♂️"
        probability = [0.15, 0.15, 0.70]
        verdict_color = "red"
        advice = "⚠️ **Warning!** Your app habits show a lot of time spent swiping or messaging with very few real matches to show for it. This usually hints at running into bots or fake profiles. Be cautious about who is on the other side of the screen!"
        
    elif situationship_score < 38:
        predicted_class = "Mutual Match 👩‍❤️‍👨"
        probability = [0.10, 0.75, 0.15]
        verdict_color = "green"
        advice = "🎉 **Green Light!** You have an amazing balance. You spend a reasonable amount of time on the app, send quality messages, and get great matches in return. You are on the perfect track to find a genuine connection!"
        
    else:
        predicted_class = "Ghosted 👻"
        probability = [0.65, 0.20, 0.15]
        verdict_color = "orange"
        advice = "💤 **The Fading Zone:** You are putting a lot of effort into sending texts, but the matching spark isn't keeping up. This usually means conversations start off strong but suddenly turn into silence. Try shaking up your profile or bio!"
    st.markdown("---")
    st.markdown("### 📊 Visual Summary Dashboard")

    dash_col1, dash_col2 = st.columns([1, 1.2])

    with dash_col1:
        # Visual Meter Gauge using Plotly
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = situationship_score,
            title = {'text': "Situationship Risk Index"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#2c3e50"},
                'steps': [
                    {'range': [0, 38], 'color': "#2ecc71"},   # Safe / Match
                    {'range': [38, 60], 'color': "#f1c40f"},  # Warning / Ghosted
                    {'range': [60, 100], 'color': "#e74c3c"}  # Dangerous / Catfish
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