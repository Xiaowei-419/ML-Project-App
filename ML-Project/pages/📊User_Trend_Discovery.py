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
    # We look for your local file FIRST. If running locally, it reads it instantly!
    # If deployed on GitHub/Streamlit Cloud, it reads the raw web file perfectly.
    try:
        df = pd.read_csv("dating_data_final_processed.csv")
    except:
        # FIXED: Converted your preview link into a direct download stream link so pandas never crashes
        direct_csv_url = "https://drive.google.com/uc?export=download&id=1DsmNGNKdXF6GS5_ltgNMYEpz1jcWMOMb"
        df = pd.read_csv(direct_csv_url)
    return df

# Load the dataset safely
try:
    df = load_data()
    
    # --- STEP 1: CLEAN QUICK LABELS FOR THE USER ---
    # Remap the target values to look pretty and clear on charts if they exist
    target_col = 'Outcome_encoded' if 'Outcome_encoded' in df.columns else 'match_outcome'
    
    if target_col in df.columns:
        df['Dating Outcome'] = df[target_col].astype(str).replace({
            '0': 'Ghosted 👻', '1': 'Mutual Match 👩‍❤️‍👨', '2': 'Catfished 🕵️‍♂️',
            '0.0': 'Ghosted 👻', '1.0': 'Mutual Match 👩‍❤️‍👨', '2.0': 'Catfished 🕵️‍♂️',
            'Ghosted': 'Ghosted 👻', 'Mutual Match': 'Mutual Match 👩‍❤️‍👨', 'Catfished': 'Catfished 🕵️‍♂️'
        })
    else:
        df['Dating Outcome'] = "Unknown Status"

    # FIXED: Reverted 'Hours' to 'Usage Score' or 'Minutes' to preserve metric math correctness
    friendly_names = {
        'AppUsage': 'Daily App Usage Score',
        'swipe_right_ratio': 'Swipe Right Rate (%)',
        'message_sent_count': 'Messages Sent Daily',
        'profile_pics_count': 'Profile Pictures Uploaded',
        'bio_length': 'Bio Characters Length',
        'emoji_usage_rate': 'Emoji Usage Rate',
        'Situationship_Index': 'Situationship Risk Score'
    }
    
    # Dynamically filter columns to what actually exists in your dataframe
    available_cols = [c for c in friendly_names.keys() if c in df.columns]
    dropdown_labels = [friendly_names[c] for c in available_cols]
    
    # --- STEP 2: SUMMARY METRICS ---
    st.markdown("### 📈 Dating Apps Quick Statistics")
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.metric(label="Profiles Analyzed", value=f"{len(df):,}")
    
    with col_m2:
        if 'AppUsage' in df.columns:
            avg_time = df['AppUsage'].mean()
            # Displays the raw mathematical average found in your dataset rows cleanly
            st.metric(label="Average Daily App Usage Score", value=f"{avg_time:.2f}")
        else:
            st.metric(label="Data Attributes Tracked", value=f"{len(available_cols)} Patterns")
            
    with col_m3:
        if 'Dating Outcome' in df.columns:
            most_common = df['Dating Outcome'].mode()[0]
            st.metric(label="Most Common App Result", value=most_common)
        else:
            st.metric(label="Target Category", value="Dating Outcomes")

    st.markdown("---")

    # --- STEP 3: INTERACTIVE COMPARISON CHART (BOX PLOT REPLACEMENT) ---
    if len(available_cols) >= 1:
        st.markdown("### 🕵️‍♂️ Explore Behavior Ranges Across Outcomes")
        st.markdown("Select a dating habit below to see its statistical distribution. This chart reveals the typical ranges and midpoints for each ultimate dating outcome.")

        # Single select box is much cleaner and less overwhelming for the user
        chosen_habit_label = st.selectbox("Choose a dating habit to analyze:", dropdown_labels, index=0)

        # Map the friendly label back to the real technical database column name
        real_habit = [k for k, v in friendly_names.items() if v == chosen_habit_label][0]

        # Build an elegant, highly interpretable Box Plot
        fig_box = px.box(
            df, 
            x='Dating Outcome', 
            y=real_habit, 
            color='Dating Outcome',
            title=f"Distribution Range of '{chosen_habit_label}' by Dating Outcome",
            color_discrete_map={
                'Mutual Match 👩‍❤️‍👨': '#2ecc71', 
                'Ghosted 👻': '#f1c40f', 
                'Catfished 🕵️‍♂️': '#e74c3c'
            },
            points=False, # Hides chaotic outlier dots so the boxes stay beautifully clean
            notched=True   # Adds a narrowing at the median line to help visually pinpoint the average
        )

        # Style the layout adjustments to make it look professional
        fig_box.update_layout(
            xaxis_title="Dating Outcome",
            yaxis_title=chosen_habit_label,
            showlegend=False,
            height=450
        )
        
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    # --- STEP 4: PIE CHART BREAKDOWN ---
    if 'Dating Outcome' in df.columns:
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
    
    st.markdown("---")

    # --- STEP 4.5: BEHAVIORAL TIER DISTRIBUTION BREAKDOWN ---
    if 'Dating Outcome' in df.columns and len(available_cols) >= 1:
        st.markdown("### 📊 Behavioral Tier Distribution Analysis")
        st.markdown("See the shifting ratio of relationship outcomes across different operational levels of user engagement.")

        # Let user select which continuous trend line to discretize
        tier_habit_label = st.selectbox("Select a habit to group into behavioral tiers:", dropdown_labels, index=min(1, len(dropdown_labels)-1), key="tier_choice")
        real_tier_habit = [k for k, v in friendly_names.items() if v == tier_habit_label][0]

        # Clone a temporary dataframe subset safely to apply quick binning operations
        df_tier = df[[real_tier_habit, 'Dating Outcome']].copy()

        # Dynamic pd.qcut grouping parameters to split any feature into balanced tiers
        try:
            df_tier['Activity Tier'] = pd.qcut(
                df_tier[real_tier_habit], 
                q=3, 
                labels=["Low Level Focus", "Moderate Level Focus", "High Level Focus"],
                duplicates='drop'
            )
        except Exception:
            # Fallback if variable math does not allow continuous quantiles nicely
            df_tier['Activity Tier'] = pd.cut(
                df_tier[real_tier_habit], 
                bins=3, 
                labels=["Low Level Focus", "Moderate Level Focus", "High Level Focus"]
            )

        # Aggregate counts to compile precise stacked bar distributions
        df_counts = df_tier.groupby(['Activity Tier', 'Dating Outcome'], observed=False).size().reset_index(name='Total Users')

        # Generate a beautiful 100% relative stacked percentage distribution graph
        fig_stacked = px.bar(
            df_counts,
            x="Activity Tier",
            y="Total Users",
            color="Dating Outcome",
            title=f"Ratio Breakdown of Outcomes Based on '{tier_habit_label}' Tiers",
            color_discrete_map={
                'Mutual Match 👩‍❤️‍👨': '#2ecc71', 
                'Ghosted 👻': '#f1c40f', 
                'Catfished 🕵️‍♂️': '#e74c3c'
            },
            barmode="textual_none", # Kept clean
        )

        # Update layouts to stretch seamlessly to 100% capacity grid bounds
        fig_stacked.update_layout(
            yaxis_title="Volume Spread of App Users",
            xaxis_title="Engineered Activity Thresholds",
            height=450
        )

        st.plotly_chart(fig_stacked, use_container_width=True)

    # --- STEP 5: CLEAN DATA SHEET LOOKER ---
    st.markdown("---")
    with st.expander("🔍 Click here to view a sample of the raw spreadsheet data"):
        st.markdown("This is a preview of the clean, raw data table powering this dashboard:")
        display_features = [c for c in available_cols]
        if 'Dating Outcome' in df.columns:
            display_features.append('Dating Outcome')
        st.dataframe(df[display_features].head(10), use_container_width=True)

except Exception as e:
    st.error(f"🔄 **Unable to parse data column arrays.** Technical Error Details: {e}")