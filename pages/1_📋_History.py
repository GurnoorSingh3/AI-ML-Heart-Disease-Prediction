import streamlit as st
import pandas as pd
from utils.styles import inject_css, sidebar_logo, divider
from utils.database import get_all_predictions, clear_all_predictions

st.set_page_config(
    page_title="CardioScan · History",
    page_icon="📋",
    layout="centered",
)

inject_css()
sidebar_logo()

# Page header 
st.markdown("""
<div class="hero">
  <span style="font-size:2.6rem; display:block; margin-bottom:.4rem;">📋</span>
  <h1>Prediction <span>History</span></h1>
  <p>All past risk assessments stored in your local database</p>
</div>
""", unsafe_allow_html=True)

# Load history from database 
divider("Past Predictions")

history = get_all_predictions()

if history:
    # Build DataFrame from raw database rows
    history_df = pd.DataFrame(history, columns=[
        "ID","Name", "Age", "Resting BP", "Cholesterol", "Max HR", "Oldpeak", "CA",
        "Sex", "Chest Pain", "FBS", "Rest ECG", "Exang", "Slope", "Thal",
        "Prediction", "Probability", "Timestamp"
    ])

    # Summary stat cards 
    total      = len(history_df)
    high_risk  = (history_df["Prediction"] == "High Risk").sum()
    low_risk   = (history_df["Prediction"] == "Low Risk").sum()
    avg_prob   = round(history_df["Probability"].mean(), 1)

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card">
        <div class="val">{total}</div>
        <div class="lbl">Total Scans</div>
      </div>
      <div class="stat-card">
        <div class="val" style="color:#A93226;">{high_risk}</div>
        <div class="lbl">High Risk</div>
      </div>
      <div class="stat-card">
        <div class="val" style="color:#1E8449;">{low_risk}</div>
        <div class="lbl">Low Risk</div>
      </div>
      <div class="stat-card">
        <div class="val">{avg_prob}%</div>
        <div class="lbl">Avg Probability</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Filters
    divider("Filter & View")

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        filter_pred = st.selectbox("Filter by Prediction", ["All", "High Risk", "Low Risk"])
    with filter_col2:
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Highest Risk", "Lowest Risk"])

    # Apply filter
    if filter_pred != "All":
        history_df = history_df[history_df["Prediction"] == filter_pred]

    # Apply sort
    if sort_by == "Newest First":
        history_df = history_df.sort_values("ID", ascending=False)
    elif sort_by == "Oldest First":
        history_df = history_df.sort_values("ID", ascending=True)
    elif sort_by == "Highest Risk":
        history_df = history_df.sort_values("Probability", ascending=False)
    elif sort_by == "Lowest Risk":
        history_df = history_df.sort_values("Probability", ascending=True)

    # Display table (selected columns only)
    display_df = history_df[[
        "Name","Age", "Sex", "Chest Pain", "Cholesterol",
        "Max HR", "Prediction", "Probability", "Timestamp"
    ]].copy()

    # Format probability as percentage string
    display_df["Probability"] = display_df["Probability"].apply(lambda x: f"{round(x,1)}%")

    # Colour the Prediction column
    def highlight_prediction(val):
        if "High Risk" in str(val):
            return "background-color: #FDEDEC; color: #A93226; font-weight: 600;"
        if "Low Risk" in str(val):
            return "background-color: #EAFAF1; color: #1E8449; font-weight: 600;"
        return ""

    styled_df = display_df.style.applymap(highlight_prediction, subset=["Prediction"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    #  Clear history button
    divider("Manage")
    st.warning("⚠️ Clearing history permanently deletes all saved predictions.")
    if st.button("🗑️  Clear All History"):
        clear_all_predictions()
        st.success("History cleared. Refresh the page to see the updated table.")

else:
    # No records yet
    st.markdown("""
    <div class="history-empty">
        📂 No prediction history yet.<br>
        <small>Go to the <strong>Home</strong> page and run your first analysis!</small>
    </div>
    """, unsafe_allow_html=True)
