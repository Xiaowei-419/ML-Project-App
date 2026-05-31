import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🕵️‍♂️ AI Detective: Decoding Your App Fate")
st.markdown("""
Have you ever wonder why some people effortlessly find romance while some end up stuck in endless talking stages, 
suddenly ghosted, or matching with suspicious fake profiles? 

Our AI detective has analyzed thousands of profiles to reveal the secret 'rules' behind dating apps. 
See exactly how your daily habits result in your dating destiny!
""")

st.markdown("---")

# --- SECTION 1: SIMPLIFIED HABIT RANKING ---
st.subheader("🏆 Green Flag vs. Red Flag Leaderboard")
st.markdown("Not all habits are equal! Here is how heavily the AI weighs your daily choices. Some habits drag you straight into a endless dating traps, while others act as a shield to protect your peace.")

importance_data = {
    "Your Dating Habits": [
        "📱 Scrolling for Hours",
        "👉 Swiping 'Yes' on Everyone",
        "💬 Sending Endless Text",
        "😂 Overusing Emojis",
        "✍️ Leaving Your Bio Blank/Short",
        "📸 Uploading Lots of Profile Pictures"
    ],
    "The AI's Take": [
        "🚨 Red Flag Warning",
        "⚠️ Major Warning Sign",
        "⏳ Minor Warning Sign",
        "ℹ️ Doesn't Matter Much",
        "🛡️ Good Profile Shield",
        "✨ Ultimate Green Flag"
    ],
    "Impact Score": [85, 65, 35, 10, -15, -45]
}

df_importance = pd.DataFrame(importance_data)

# Create a clean, visually simple bar chart
fig_importance = px.bar(
    df_importance,
    x="Impact Score",
    y="Your Dating Habits",
    orientation="h",
    color="The AI's Take",
    color_discrete_map={
        "✨ Ultimate Green Flag": "#2ecc71",
        "🛡️ Good Profile Shield": "#27ae60",
        "ℹ️ Doesn't Matter Much": "#95a5a6",
        "⏳ Minor Warning Sign": "#f1c40f",
        "⚠️ Major Warning Sign": "#e67e22",
        "🚨 Red Flag Warning": "#e74c3c"
    },
    labels={"Impact Score": "Habit Power Level"},
    title="Which Habits Hurt Your Chances vs. Help You Win"
)

fig_importance.update_layout(
    showlegend=True, 
    height=380, 
    yaxis_autorange="reversed",
    xaxis_title="← Helps You Match | Pulls You into Traps →"
)
st.plotly_chart(fig_importance, use_container_width=True)

st.markdown("---")

# --- SECTION 2: THE SIMPLE INTERACTIVE "MYSTIC BALL" RULE SIMULATOR ---
st.subheader("🔮 Predict Your App Fate")
st.markdown("Adjust the sliders below to tell us your dating style. The AI Detective will predict where that profile will end up!")

sim_col1, sim_col2 = st.columns([1, 1.2])

with sim_col1:
    with st.container(border=True):
        st.markdown("#### 🎛️ Choose a Dating Style")
        app_activity = st.select_slider(
            "⏱️ Daily Screen Time:",
            options=["Just a few minutes", "Under an hour", "Hours and hours!"],
            value="Under an hour"
        )
        
        swiping_habit = st.select_slider(
            "🎲 Swiping Strategy:",
            options=["Super Picky", "Healthy Balance", "Swiping 'Right' on everyone"],
            value="Healthy Balance"
        )

        # Map simple friendly selections back to background rule values safely
        score = 50 
        if app_activity == "Just a few minutes": score -= 20
        if app_activity == "Hours and hours!": score += 25
        
        if swiping_habit == "Super Picky": score -= 15
        if swiping_habit == "Swiping 'Right' on everyone": score += 20

with sim_col2:
    st.markdown("#### 🤖 The Detective's Prediction")
    
    if score > 60:
        st.error("### 🕵️‍♂️ High Catfish & Bot Danger Zone!")
        st.info("🚨 **What's happening here :** When a profile spends hours on end rapidly swiping 'yes' on everyone, the algorithm flags this as machine-like behavior. Our data shows this hyperactive and unselective pattern is highly vulnerable to falling into fake profile traps, scam bots, and catfished.")
    elif score < 38:
        st.success("### 👩‍❤️‍👨 Green Flags! Safe Track to a Mutual Match")
        st.info("✨ **What's happening here :** Low screen time mixed with selective swiping shows true intent. The data confirms this thoughtful approach yields the highest success rate for transforming into a meaningful real-life connection.")
    else:
        st.warning("### 👻 The Fading Loop (High Risk of Being Ghosted)")
        st.info("💤 **What's happening here :** This represents a casual and typical user pattern. While you are active enough to spark a conversation, the habits lack the momentum needed and most probably fizzle out into absolute silence.")

st.markdown("---")

# --- SECTION 3: PLAIN ENGLISH ACADEMIC TAKEAWAY ---
st.subheader("💡 Tips to Success")

col_t1, col_t2 = st.columns(2)
with col_t1:
    with st.container(border=True):
        st.markdown("### What Ruins Your Chances?")
        st.markdown("""
        * **Mindless App Usage :** Leaving the app open for hours treating it like an endless social media scrolling feed ruins your match algorithm placement.
        * **Mystery Profiles :** Leaving your bio empty flags you immediately as a low-effort profile or a potential spam bot.
        """)

with col_t2:
    with st.container(border=True):
        st.markdown("###  What Actually Works?")
        st.markdown("""
        * **Quality Over Quantity :** Being highly selective will match you with premium and active users.
        * **Show Yourself :** Upload more profile pictures to show your personalities. Providing natural conversation starters.
        """)