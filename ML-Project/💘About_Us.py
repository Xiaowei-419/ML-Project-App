import streamlit as st

st.set_page_config(
    page_title="Tying the (Data) Knot",
    page_icon="💘",
    layout="wide"
)

# Title & Intro
st.title("Decoding the Situationship: Predicting Dating App Destinies with the Situationship Index")
st.subheader("Machine Learning Project (WIA1006)")

st.markdown("""
### 📖 Project Overview
In this era, modern relationships highly depend on digital interactions. 
This application uses Machine Learning Models to translate behaviors such as app usage patterns, messaging habits, 
and swipe behaviors into predictable relationship trajectories.

By examining interaction signals, we explore phenomena such as **Ghosting**, **Catfishing**, and **Mutual Matches**, 
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
st.markdown("### 👥 Meet Our Team")

# Straightforward row-by-row layout
with st.container(border=True):
    st.markdown("### 👤 Chua Bi Yun")
    st.markdown("**Role:** Data Architect | **Matric No:** 25005610")

with st.container(border=True):
    st.markdown("### 👤 Phong Xiao Wei")
    st.markdown("**Role:** Algorithm Specialist | **Matric No:** 25005900")

with st.container(border=True):
    st.markdown("### 👤 Joyce Wong Tze Eng")
    st.markdown("**Role:** ML Engineer | **Matric No:** 25005859")

with st.container(border=True):
    st.markdown("### 👤 Choo Kah Lok")
    st.markdown("**Role:** ML Engineer | **Matric No:** 25005750")

with st.container(border=True):
    st.markdown("### 👤 Chai Xin Tong")
    st.markdown("**Role:** Visual Analyst | **Matric No:** 25005524")