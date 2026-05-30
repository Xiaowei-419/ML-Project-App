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
In this digital era, modern relationships highly dependence on digital interactions. 
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

# Adjust columns depending on your team size (e.g., 3 or 4)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140037.png", width=120) # Dummy avatar
    st.markdown("**Chua Bi Yun**")
    st.caption("Data Architect")
    st.text("Matric No: 25005610")

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=120)
    st.markdown("**Phong Xiao Wei**")
    st.caption("Algorithm Specialist")
    st.text("Matric No: 25005900")

with col3:
    st.image("https://cdn-icons-png.flaticon.com/512/4139/4139981.png", width=120)
    st.markdown("**Joyce Wong Tze Eng**")
    st.caption("ML Engineer")
    st.text("Matric No: 25005859")

with col4:
    st.image("https://cdn-icons-png.flaticon.com/512/4139/4139981.png", width=120)
    st.markdown("**Choo Kah Lok**")
    st.caption("ML Engineer")
    st.text("Matric No: 25005750")

with col5:
    st.image("https://cdn-icons-png.flaticon.com/512/4139/4139981.png", width=120)
    st.markdown("**Chai Xin Tong**")
    st.caption("Visual Analyst")
    st.text("Matric No: 25005524")