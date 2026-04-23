import streamlit as st
import pickle
import pandas as pd
from utils.styles import inject_css, sidebar_logo, divider
from utils.database import init_db, save_prediction

st.set_page_config(layout="wide")
# ── Page config 
st.set_page_config(
    page_title="CardioScan · Home",
    page_icon="🫀",
    layout="centered",
)

inject_css()
sidebar_logo()

# ── Load model & scaler 
@st.cache_resource
def load_artifacts():
    with open("heart_disease_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_artifacts()

# ── Initialise the SQLite database 
init_db()

# ── Hero banner 
st.markdown("""
<div class="hero">
  <span class="hero-icon">🫀</span>
  <h1>Cardio<span>Scan</span></h1>
  <p>AI-powered heart disease risk assessment · UCI Heart Dataset · Random Forest</p>
</div>
""", unsafe_allow_html=True)

# ── Patient input form ────────────────────────────────────────────────────────
divider("Patient Information")

col1, col2 = st.columns(2)

with col1:
    patient_name = st.text_input("Patient Name",placeholder="Enter full name")
    age      = st.number_input("Age (years)",                    min_value=1,   max_value=120, value=50)
    trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=0,   max_value=300, value=120)
    chol     = st.number_input("Cholesterol (mg/dl)",            min_value=0,   max_value=700, value=200)
    thalch   = st.number_input("Max Heart Rate Achieved",        min_value=0,   max_value=300, value=150)
    oldpeak  = st.number_input("Oldpeak (ST depression)",        min_value=-5.0,max_value=10.0,value=0.0, step=0.1)
    ca       = st.selectbox("Major Vessels (0–3)", [0, 1, 2, 3])

with col2:
    sex     = st.selectbox("Sex",                         ["Female", "Male"])
    cp      = st.selectbox("Chest Pain Type",             ["asymptomatic", "atypical angina", "non-anginal", "typical angina"])
    fbs     = st.selectbox("Fasting Blood Sugar > 120",   [False, True])
    restecg = st.selectbox("Resting ECG",                 ["lv hypertrophy", "normal", "st-t abnormality"])
    exang   = st.selectbox("Exercise-Induced Angina",     [False, True])
    slope   = st.selectbox("Slope of ST Segment",         ["downsloping", "flat", "upsloping"])
    thal    = st.selectbox("Thalassemia",                 ["fixed defect", "normal", "reversable defect"])

divider("Run Analysis")
predict_btn = st.button("🔍  Analyse Risk")

# ── Prediction logic (runs only when button is clicked) ───────────────────────
if predict_btn:

    # 1. Build empty DataFrame with exact columns the model expects
    input_data = pd.DataFrame(columns=model.feature_names_in_)
    input_data.loc[0] = 0  # fill all columns with 0

    # 2. Fill numerical values directly
    input_data["age"]      = age
    input_data["trestbps"] = trestbps
    input_data["chol"]     = chol
    input_data["thalch"]   = thalch
    input_data["oldpeak"]  = oldpeak
    input_data["ca"]       = ca

    # 3. One-hot encode categorical inputs (replicates pd.get_dummies with drop_first=True)
    if sex == "Male":
        input_data["sex_Male"] = 1

    cp_map = {
        "atypical angina": "cp_atypical angina",
        "non-anginal":     "cp_non-anginal",
        "typical angina":  "cp_typical angina",
    }
    if cp in cp_map:
        input_data[cp_map[cp]] = 1

    if fbs:
        input_data["fbs_True"] = 1

    restecg_map = {
        "normal":           "restecg_normal",
        "st-t abnormality": "restecg_st-t abnormality",
    }
    if restecg in restecg_map:
        input_data[restecg_map[restecg]] = 1

    if exang:
        input_data["exang_True"] = 1

    slope_map = {"flat": "slope_flat", "upsloping": "slope_upsloping"}
    if slope in slope_map:
        input_data[slope_map[slope]] = 1

    thal_map = {"normal": "thal_normal", "reversable defect": "thal_reversable defect"}
    if thal in thal_map:
        input_data[thal_map[thal]] = 1

    # 4. Scale numerical columns using the saved StandardScaler
    num_cols = ["age", "trestbps", "chol", "thalch", "oldpeak", "ca"]
    input_data[num_cols] = scaler.transform(input_data[num_cols])

    # 5. Get prediction and probability
    pred     = model.predict(input_data)[0]           # 0 or 1
    proba    = model.predict_proba(input_data)[0]     # [prob_no_disease, prob_disease]
    risk_pct = round(proba[1] * 100, 1)               # e.g. 73.4

    # 6. Save to database
    prediction_label = "High Risk" if pred == 1 else "Low Risk"
    save_prediction(
        patient_name,age, trestbps, chol, thalch, oldpeak, ca,
        sex, cp, fbs, restecg, exang, slope, thal,
        prediction_label, risk_pct
    )

    # 7. Show result card
    if pred == 1:
        st.markdown(f"""
        <div class="result-card danger">
          <div class="icon">⚠️</div>
          <div class="content">
            <h3>Elevated Risk Detected</h3>
            <p>The model indicates a <strong>{risk_pct}%</strong> probability of heart disease
               based on the provided clinical parameters. Please consult a cardiologist
               for a thorough evaluation.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)
        fill_class = "danger"
    else:
        st.markdown(f"""
        <div class="result-card safe">
          <div class="icon">✅</div>
          <div class="content">
            <h3>Low Risk Detected</h3>
            <p>The model indicates a <strong>{risk_pct}%</strong> probability of heart disease.
               Risk appears low, but regular check-ups are still recommended.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)
        fill_class = "safe"

    # 8. Probability bar
    st.markdown(f"""
    <div class="prob-row">
      <div class="prob-label">
        <span>Risk Probability</span>
        <span>{risk_pct}%</span>
      </div>
      <div class="prob-track">
        <div class="prob-fill {fill_class}" style="width:{risk_pct}%;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 9. Disclaimer
    st.markdown("""
    <div class="disclaimer">
      ⚕️ <strong>Medical Disclaimer:</strong> This tool is for educational and research
      purposes only. It does not constitute medical advice, diagnosis, or treatment.
      Always consult a qualified healthcare professional.
    </div>
    """, unsafe_allow_html=True)
