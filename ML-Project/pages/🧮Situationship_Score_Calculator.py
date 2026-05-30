import streamlit as st

st.set_page_config(page_title="Situationship Calculator", page_icon="🧮")
st.title("🧮 Situationship Score Calculator")

st.markdown("""
Have you ever wonder why some matches lead to great dates while some get stuck? 
This calculator uses our **Machine Learning Innovation Feature** to measure your online dating habits 
and tell you if your current behavior puts you in the **Situationship Zone**!
""")

with st.form("index_calculator"):
    st.markdown("### 📱 Tell Us About Your Dating App Habits")
    
    # 1. Inputs converted to clear real-world representations
    app_usage_hours = st.slider("How many hours do you spend on the app daily?", 0.0, 10.0, 2.5, step=0.5)
    swipe_ratio_pct = st.slider("Out of 100 profiles, how many do you swipe RIGHT (Accept) on?", 0, 100, 40)
    
    col1, col2 = st.columns(2)
    with col1:
        likes_received = st.number_input("Estimated total likes you have received:", min_value=0, value=50)
    with col2:
        mutual_matches = st.number_input("How many total mutual matches have you made?", min_value=0, value=10)
        
    submitted = st.form_submit_button("Calculate My Score ✨")

if submitted:
    # --- BACKEND ML MATHEMATICAL COMPLIANCE CONVERSIONS ---
    # Convert hours to minutes and clip within dataset ranges to normalize (MinMaxScaler replication)
    norm_app_usage = min(max((app_usage_hours * 60) / 360.0, 0.0), 1.0) 
    norm_swipe_ratio = swipe_ratio_pct / 100.0
    
    # Replicating your notebook's exact engineered calculations (Cell 6)
    match_rate = mutual_matches / (likes_received + 1)
    match_rate = min(max(match_rate, 0.0), 1.0)
    
    efficiency = mutual_matches / (norm_app_usage + 0.1)
    efficiency = min(max(efficiency, 0.0), 1.0)
    
    # Notebook formula: 100 * (0.35 * AppUsage + 0.25 * SwipeRatio + 0.25 * (1-MatchRate) + 0.15 * (1-Efficiency))
    situationship_score = 100 * (
        (0.35 * norm_app_usage) + 
        (0.25 * norm_swipe_ratio) + 
        (0.25 * (1.0 - match_rate)) + 
        (0.15 * (1.0 - efficiency))
    )
    
    st.markdown("---")
    st.subheader("🎉 Your Results")
    st.metric(label="Your Final Situationship Score", value=f"{situationship_score:.1f} / 100")
    
    # --- USER-FRIENDLY INSIGHT CARDS ---
    if situationship_score > 65:
        st.success("🔥 **Great Match Potential!** You are using the app actively and successfully converting your swipes into real connections.")
    elif situationship_score >= 40:
        st.warning("⚠️ **Stuck in the 'Situationship' Zone!** Plenty of effort is being made, but your matches are staying in the casual, ambiguous phase.")
    else:
        st.error("📉 **Low Connection Spark!** Very little activity or low response rates. Your conversations are at a high risk of going cold.")