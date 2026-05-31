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

# Top Row: 3 Columns
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.markdown("#### Chua Bi Yun")
    st.caption("*Data Architect*")
    st.code("25005610", language="text")

with row1_col2:
    st.markdown("#### Phong Xiao Wei")
    st.caption("*Algorithm Specialist*")
    st.code("25005900", language="text")

with row1_col3:
    st.markdown("#### Joyce Wong Tze Eng")
    st.caption("*ML Engineer*")
    st.code("25005859", language="text")

st.markdown("<br>", unsafe_allow_html=True) # Adds elegant structural vertical spacing between card layers

# Bottom Row: 3 Columns
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.markdown("#### Choo Kah Lok")
    st.caption("*ML Engineer*")
    st.code("25005750", language="text")

with row2_col2:
    st.markdown("#### Chai Xin Tong")
    st.caption("*Visual Analyst*")
    st.code("25005524", language="text")

with row2_col3:
    # Keeps alignment empty & pristine if you have a 5-member configuration group
    st.write("")