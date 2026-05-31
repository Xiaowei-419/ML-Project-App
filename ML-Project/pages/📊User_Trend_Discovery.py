import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dating Trends Insights", page_icon="📊", layout="wide")

# User-Friendly Header
st.title("📊 Online Dating Trends & Insights")
st.markdown("""
Welcome to the Data Discovery Center! Here, we look at the real data patterns of about thousands of app users. 
Use this page to see how daily habits like swiping and texting directly lead to matching up, 
getting ghosted, or running into misleading profiles!
""")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dating_data_final_processed.csv")
    except:
        direct_csv_url = "https://drive.google.com/uc?export=download&id=1DsmNGNKdXF6GS5_ltgNMYEpz1jcWMOMb"
        df = pd.read_csv(direct_csv_url)
    return df

# Load the dataset safely
try:
    df = load_data()
    
    # --- STEP 1: CLEAN QUICK LABELS FOR THE USER ---
    target_col = 'Outcome_encoded' if 'Outcome_encoded' in df.columns else 'match_outcome'
    
    if target_col in df.columns:
        df['Dating Outcome'] = df[target_col].astype(str).replace({
            '0': 'Ghosted 👻', '1': 'Mutual Match 👩‍❤️‍👨', '2': 'Catfished 🕵️‍♂️',
            '0.0': 'Ghosted 👻', '1.0': 'Mutual Match 👩‍❤️‍👨', '2.0': 'Catfished 🕵️‍♂️',
            'Ghosted': 'Ghosted 👻', 'Mutual Match': 'Mutual Match 👩‍❤️‍👨', 'Catfished': 'Catfished 🕵️‍♂️'
        })
    else:
        df['Dating Outcome'] = "Unknown Status"

    friendly_names = {
        'AppUsage': 'Daily App Usage Score',
        'swipe_right_ratio': 'Swipe Right Rate (%)',
        'message_sent_count': 'Messages Sent Daily',
        'profile_pics_count': 'Profile Pictures Uploaded',
        'bio_length': 'Bio Characters Length',
        'emoji_usage_rate': 'Emoji Usage Rate',
        'Situationship_Index': 'Situationship Risk Score'
    }
    
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

    # --- STEP 3: INTERACTIVE COMPARISON CHART (DYNAMIC MULTI-FEATURE BAR CHART) ---
    if len(available_cols) >= 1:
        st.markdown("### 🎛️ Dynamic Behavioral Profile Builder")
        st.markdown("Check or uncheck the features below to build your own custom comparison chart. This view uses normalization to drastically amplify the hidden differences between outcomes.")

        # Interactive Checklist Filter for Features
        selected_labels = st.multiselect(
            "Select which features you want to compare on the chart:",
            options=dropdown_labels,
            default=dropdown_labels[:4]  # Pre-selects the first 4 features by default
        )

        if not selected_labels:
            st.warning("⚠️ Please select at least one feature from the filter above to display the visual chart!")
        else:
            # Map selected friendly labels back to the real technical database column names
            selected_real_cols = [k for k, v in friendly_names.items() if v in selected_labels]

            # 1. Calculate the mean for the selected features grouped by Outcome
            df_bar_raw = df.groupby('Dating Outcome')[selected_real_cols].mean().reset_index()

            # 2. Apply Min-Max Scaling to blow up and amplify the visual differences
            df_bar_scaled = df_bar_raw.copy()
            for col in selected_real_cols:
                col_min = df_bar_raw[col].min()
                col_max = df_bar_raw[col].max()
                if col_max != col_min:
                    df_bar_scaled[col] = (df_bar_raw[col] - col_min) / (col_max - col_min)
                else:
                    df_bar_scaled[col] = 0.5

            # 3. Melt the data frame into a clean structural format for Plotly Express
            df_bar_melted = df_bar_scaled.melt(
                id_vars='Dating Outcome', 
                value_vars=selected_real_cols,
                var_name='Habit Attribute', 
                value_name='Relative Intensity'
            )

            # 4. Map back the technical column names to our clean, user-friendly labels
            df_bar_melted['Habit Label'] = df_bar_melted['Habit Attribute'].map(friendly_names)

            # 5. Build a grouped side-by-side Horizontal Bar Chart
            fig_filtered_bar = px.bar(
                df_bar_melted,
                y='Habit Label',
                x='Relative Intensity',
                color='Dating Outcome',
                barmode='group',  # Places the three outcome bars side-by-side for each feature
                orientation='h',  # Horizontal orientation makes text labels incredibly easy to read
                title="Amplified Contrast Analysis Across Selected Features",
                color_discrete_map={
                    'Mutual Match 👩‍❤️‍👨': '#2ecc71', 
                    'Ghosted 👻': '#f1c40f', 
                    'Catfished 🕵️‍♂️': '#e74c3c'
                },
                labels={'Relative Intensity': 'Relative Intensity (Min-Max Scaled Diff)'}
            )

            # Make the bars look highly professional and clear
            fig_filtered_bar.update_layout(
                yaxis_title="",
                xaxis_title="Relative Scaling (Higher means group scores highest for this feature)",
                height=150 + (len(selected_labels) * 80),  # Dynamically expands taller if user selects more features!
                legend_title_text='Dating Outcome',
                xaxis=dict(showticklabels=False)  # Hides numeric decimals since it represents relative scale
            )

            st.plotly_chart(fig_filtered_bar, use_container_width=True)

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

        tier_habit_label = st.selectbox("Select a habit to group into behavioral tiers:", dropdown_labels, index=min(1, len(dropdown_labels)-1), key="tier_choice")
        real_tier_habit = [k for k, v in friendly_names.items() if v == tier_habit_label][0]

        df_tier = df[[real_tier_habit, 'Dating Outcome']].copy()

        try:
            df_tier['Activity Tier'] = pd.qcut(
                df_tier[real_tier_habit], 
                q=3, 
                labels=["Low Level Focus", "Moderate Level Focus", "High Level Focus"],
                duplicates='drop'
            )
        except Exception:
            df_tier['Activity Tier'] = pd.cut(
                df_tier[real_tier_habit], 
                bins=3, 
                labels=["Low Level Focus", "Moderate Level Focus", "High Level Focus"]
            )

        df_counts = df_tier.groupby(['Activity Tier', 'Dating Outcome'], observed=False).size().reset_index(name='Total Users')

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
            barmode="stack" 
        )

        fig_stacked.update_layout(
            barnorm="percent",
            yaxis_title="Percentage Share (%)",
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