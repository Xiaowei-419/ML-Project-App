import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dating Trends Insights", page_icon="📊", layout="wide")

# User-Friendly Header
st.title("📊 Online Dating Trends & Insights")
st.markdown("""
Welcome to the data discovery center! Here, we look at the real data patterns of thousands of app users. 
Use this dashboard to see how daily habits like swiping and texting directly lead to matching up, 
getting ghosted, or running into misleading profiles!
""")

@st.cache_data
def load_data():
    # This URL forces Google Drive to deliver the raw CSV data directly to pandas
    direct_csv_url = "https://drive.google.com/uc?export=download&id=1oR32oFLa1yX4R-jx3x0A0b9KTurT_Sa5"
    df = pd.read_csv(direct_csv_url)
    return df

# Load the dataset safely
try:
    df = load_data()
    
    # --- STEP 1: CLEAN QUICK LABELS FOR THE USER ---
    # Remap the target values to look pretty and clear on charts if they exist
    target_col = 'match_outcome' if 'match_outcome' in df.columns else 'Outcome_encoded'
    
    if target_col in df.columns:
        # Create a user-friendly display column so charts show nice names
        df['Dating Outcome'] = df[target_col].astype(str).replace({
            '0': 'Ghosted 👻', '1': 'Mutual Match 👩‍❤️‍👨', '2': 'Catfished 🕵️‍♂️',
            '0.0': 'Ghosted 👻', '1.0': 'Mutual Match 👩‍❤️‍👨', '2.0': 'Catfished 🕵️‍♂️'
        })
    else:
        df['Dating Outcome'] = "Unknown Status"

    # Human-friendly dictionary to rename ugly database column names into simple English
    friendly_names = {
        'AppUsage': 'Daily App Time (Minutes)',
        'SwipeRatio': 'Right-Swipe Rate (%)',
        'MessagesSent': 'Texts Sent Daily',
        'GhostRate': 'Past Ghosted Rate',
        'Situationship_Index': 'Situationship Risk Score'
    }
    
    # Filter columns to only what we care about and rename them for the dropdowns
    available_cols = [c for c in df.columns if c in friendly_names.keys()]
    
    # --- STEP 2: SUMMARY METRICS ---
    st.markdown("### 📈 Dating App Quick Stats")
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.metric(label="Profiles Analyzed", value=f"{len(df):,}", help="The total number of user histories calculated by our system.")
    
    with col_m2:
        if 'AppUsage' in df.columns:
            # Reversing normalizer math if needed, or keeping clean decimal representation
            avg_time = df['AppUsage'].mean()
            st.metric(label="Average Daily Screen Time", value=f"{avg_time:.1f} mins")
        else:
            st.metric(label="Data Attributes Tracked", value=f"{len(available_cols)} Patterns")
            
    with col_m3:
        if 'Dating Outcome' in df.columns:
            most_common = df['Dating Outcome'].mode()[0]
            st.metric(label="Most Common App Result", value=most_common)
        else:
            st.metric(label="Target Category", "Dating Outcomes")

    st.markdown("---")

    # --- STEP 3: INTERACTIVE COMPARISON CHART ---
    st.markdown("### 🕵️‍♂️ Compare Two Dating Habits")
    st.markdown("Pick any two dating habits below to see how they interact. Each dot is a real user profile, colored by their ultimate dating fate!")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        # User picks a clean name, we map it back to the real column behind the scenes
        chosen_x_label = st.selectbox("Choose the first habit (X-Axis):", list(friendly_names.values()), index=0)
    with col_s2:
        chosen_y_label = st.selectbox("Choose the second habit (Y-Axis):", list(friendly_names.values()), index=min(1, len(friendly_names)-1))

    # Get the real technical database column names from the friendly labels chosen
    real_x = [k for k, v in friendly_names.items() if v == chosen_x_label][0]
    real_y = [k for k, v in friendly_names.items() if v == chosen_y_label][0]

    # Build an interactive scatter plot
    fig_scatter = px.scatter(
        df, 
        x=real_x, 
        y=real_y, 
        color='Dating Outcome',
        labels={real_x: chosen_x_label, real_y: chosen_y_label},
        title=f"How '{chosen_x_label}' relates to '{chosen_y_label}'",
        color_discrete_map={'Mutual Match 👩‍❤️‍👨': '#2ecc71', 'Ghosted 👻': '#f1c40f', 'Catfished 🕵️‍♂️': '#e74c3c'},
        opacity=0.7
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # --- STEP 4: PIE CHART BREAKDOWN ---
    st.markdown("### 🗺️ The Ultimate Outcome Breakdown")
    st.markdown("What percentage of users actually land a real match versus falling into dating traps?")
    
    fig_pie = px.pie(
        df, 
        names='Dating Outcome', 
        hole=0.4,
        color='Dating Outcome',
        color_discrete_map={'Mutual Match 👩‍❤️‍👨': '#2ecc71', 'Ghosted 👻': '#f1c40f', 'Catfished 🕵️‍♂️': '#e74c3c'}
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # --- STEP 5: CLEAN DATA SHEET LOOKER ---
    st.markdown("---")
    with st.expander("🔍 Click here to view a sample of the raw spreadsheet data"):
        st.markdown("This is a preview of the clean, raw data table powering this dashboard:")
        st.dataframe(df[available_cols + ['Dating Outcome']].head(10), use_container_width=True)

except Exception as e:
    st.error("🔄 **Unable to load connection data.** Please verify your Google Drive sharing access settings are set to 'Anyone with the link'!")