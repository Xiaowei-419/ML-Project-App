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
        'Situationship_Index': 'Situationship Index'
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
        st.markdown("Filter the features below to build your own custom comparison chart. This view uses normalization to drastically amplify the hidden differences between outcomes.")

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
                barmode='group',  
                orientation='h',  
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
                height=150 + (len(selected_labels) * 80),  
                legend_title_text='Dating Outcome',
                xaxis=dict(showticklabels=False)  
            )

            st.plotly_chart(fig_filtered_bar, use_container_width=True)

    st.markdown("---")

    # --- STEP 3.5: INTERACTIVE COMPARISON CHART (RADAR BEHAVIORAL PROFILE) ---
    if len(available_cols) >= 3:
        st.markdown("### 🕸️ Algorithmic Behavioral Fingerprints")
        st.markdown("This holistic view visualizes how all user habits combine simultaneously. By normalizing the attributes, we expose the unmistakable geometric 'fingerprint' unique to each dating destiny.")

        # 1. Group by outcome and calculate the mean for all numerical available columns
        df_radar_raw = df.groupby('Dating Outcome')[available_cols].mean().reset_index()

        # 2. Apply Min-Max Scaling on the averages to drastically amplify hidden visual differences
        df_radar_scaled = df_radar_raw.copy()
        for col in available_cols:
            col_min = df_radar_raw[col].min()
            col_max = df_radar_raw[col].max()
            if col_max != col_min:
                df_radar_scaled[col] = (df_radar_raw[col] - col_min) / (col_max - col_min)
            else:
                df_radar_scaled[col] = 0.5

        # 3. Melt the data frame so it fits Plotly Express's expected structural format
        df_radar_melted = df_radar_scaled.melt(
            id_vars='Dating Outcome', 
            value_vars=available_cols,
            var_name='Habit Attribute', 
            value_name='Relative Intensity'
        )

        # 4. Map back the technical column names to our clean, user-friendly labels
        df_radar_melted['Habit Label'] = df_radar_melted['Habit Attribute'].map(friendly_names)

        # 5. Build the elegant, highly contrastive Radar Map
        fig_radar = px.line_polar(
            df_radar_melted, 
            r='Relative Intensity', 
            theta='Habit Label', 
            color='Dating Outcome',
            line_close=True,
            title="How the Machine Learning Model Separates Class Profiles",
            color_discrete_map={
                'Mutual Match 👩‍❤️‍👨': '#2ecc71', 
                'Ghosted 👻': '#f1c40f', 
                'Catfished 🕵️‍♂️': '#e74c3c'
            },
            template="plotly_white"
        )

        # 6. FIXED: Fill inside area using standard polar coordinate parameters
        fig_radar.update_traces(fill='toself')

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], showticklabels=False)
            ),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

        # --- NEW PLAIN-ENGLISH RADAR EXPLANATION BOX ---
        st.info("""
        💡 **How to read this web graph:**
        
        Instead of looking at exact statistics, this chart tracks **territory and shapes**. The further a color spikes out toward an edge, the higher that group scores for that habit. 
        
        * 🟩 **The Mutual Match Shape (Top & Right Side):** Notice how the green area balloons toward **Daily App Usage**, **Messages Sent**, and **Profile Pics**. This means successful matches come from highly active, talkative, and visually complete profiles.
        * 🟥 **The Catfished Shape (Left Side):** The red territory punches aggressively out toward the **Situationship Index** and **Emoji Usage**, but completely shrinks away from bio lengths. This is a classic bot or scam signature.
        * 🟨 **The Ghosted Shape (Bottom Spike):** The yellow area stretches directly down toward **Bio Characters Length**. This reveals that ghosted users put high effort into writing massive biographies, but score too low on daily app presence to keep the spark alive.
        """)

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