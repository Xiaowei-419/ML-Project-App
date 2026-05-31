import streamlit as st

st.set_page_config(
    page_title="Tying the (Data) Knot",
    page_icon="💘",
    layout="wide"
)

# Title & Intro
st.title("Decoding Situationship: Predicting Dating App Destinies with Situationship Index")
st.subheader("Machine Learning Group Project (WIA1006)")

st.markdown("""
### 📖 Project Overview
In this era, modern relationships highly depend on digital interactions. 
This application uses Machine Learning Models to translate behaviors such as app usage patterns, messaging habits, 
and swipe behaviors into predictable relationship trajectories.

By examining interaction signals, we explored phenomena such as **Ghosting**, **Catfishing**, and **Mutual Matches**, 
giving a structural shape to the ambiguous concept of a **'Situationship'**.
""")

# Quick Navigation Buttons / Project Links
st.markdown("---")
st.markdown("### 🔗 Project Resources")
col_link1, col_link2 = st.columns(2)
with col_link1:
    st.link_button("🌐 View Source Dataset on Kaggle", "https://www.kaggle.com/datasets/keyushnisar/dating-app-behavior-dataset", use_container_width=True)
with col_link2:
    st.info("💡 Use the sidebar menu to navigate across different modules of the system.")

# Team Members section
st.markdown("---")
st.markdown("### 👥 Our Team")

col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns(5)

with col_t1:
    st.markdown("##### **Chua Bi Yun**")
    st.caption("25005610\n\nData Architect")

with col_t2:
    st.markdown("##### **Phong Xiao Wei**")
    st.caption("25005900\n\nAlgorithm Specialist")

with col_t3:
    st.markdown("##### **Joyce Wong Tze Eng**")
    st.caption("25005859\n\nML Engineer")

with col_t4:
    st.markdown("##### **Choo Kah Lok**")
    st.caption("25005750\n\nML Engineer")

with col_t5:
    st.markdown("##### **Chai Xin Tong**")
    st.caption("25005524\n\nVisual Analyst")