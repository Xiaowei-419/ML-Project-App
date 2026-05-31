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

# Everything inside a single block to guarantee perfect baseline alignment
st.markdown("""
&nbsp;&nbsp;**Chua Bi Yun** &nbsp;&nbsp;|&nbsp;&nbsp; :gray[Data Architect] &nbsp;&nbsp;|&nbsp;&nbsp; `25005610`  

&nbsp;&nbsp;**Phong Xiao Wei** &nbsp;&nbsp;|&nbsp;&nbsp; :gray[Algorithm Specialist] &nbsp;&nbsp;|&nbsp;&nbsp; `25005900`  

&nbsp;&nbsp;**Joyce Wong Tze Eng** &nbsp;&nbsp;|&nbsp;&nbsp; :gray[ML Engineer] &nbsp;&nbsp;|&nbsp;&nbsp; `25005859`  

&nbsp;&nbsp;**Choo Kah Lok** &nbsp;&nbsp;|&nbsp;&nbsp; :gray[ML Engineer] &nbsp;&nbsp;|&nbsp;&nbsp; `25005750`  

&nbsp;&nbsp;**Chai Xin Tong** &nbsp;&nbsp;|&nbsp;&nbsp; :gray[Visual Analyst] &nbsp;&nbsp;|&nbsp;&nbsp; `25005524`  
""")