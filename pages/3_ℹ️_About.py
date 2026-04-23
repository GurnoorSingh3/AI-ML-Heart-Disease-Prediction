import streamlit as st
from utils.styles import inject_css, sidebar_logo, divider

st.set_page_config(
    page_title="CardioScan · About",
    page_icon="ℹ️",
    layout="centered",
)

inject_css()
sidebar_logo()

# Page header
st.markdown("""
<div class="hero">
  <span style="font-size:2.6rem; display:block; margin-bottom:.4rem;">ℹ️</span>
  <h1>About <span>CardioScan</span></h1>
  <p>Project overview, methodology, and references</p>
</div>
""", unsafe_allow_html=True)

# Project Overview 
divider("Project Overview")

st.markdown("""
<div class="feature-card">
  <h4>🎯 Objective</h4>
  <p>CardioScan is a machine learning–powered web application that predicts the
  likelihood of heart disease in a patient based on 13 clinical parameters.
  It was developed as a major graded project for a Computer Applications programme,
  combining data science, model development, and full-stack deployment.</p>
</div>

<div class="feature-card">
  <h4>📦 Dataset</h4>
  <p>The model is trained on the <strong>UCI Heart Disease Dataset</strong> (combined
  Cleveland, Hungary, Switzerland, and VA Long Beach sources) — ~900+ patient records with 13–14 clinical features. 
  The target variable <code>num</code> is binarised:
  0 = no disease, 1 = disease present.</p>
</div>
""", unsafe_allow_html=True)

#ML Pipeline
divider("ML Pipeline")

st.markdown("""
<div class="feature-card">
  <h4>🔄 Data Preprocessing</h4>
  <p>
    • Missing numerical values filled with <strong>median</strong><br>
    • Missing categorical values filled with <strong>mode</strong><br>
    • Categorical features one-hot encoded using <code>pd.get_dummies(drop_first=True)</code><br>
    • Numerical features standardised with <code>StandardScaler</code>
  </p>
</div>

<div class="feature-card">
  <h4>🌲 Model — Random Forest Classifier</h4>
  <p>
    • <strong>n_estimators = 200</strong> (200 decision trees in the forest)<br>
    • <strong>random_state = 42</strong> (for reproducibility)<br>
    • Train / Test split: <strong>80% / 20%</strong> with stratification<br>
    • Serialised to <code>heart_disease_model.pkl</code> using Python's <code>pickle</code>
  </p>
</div>

<div class="feature-card">
  <h4>📊 Evaluation Results</h4>
  <p>
    • Accuracy: ~94% on unseen test data <br>
    • Recall (Disease Class): ~92–95% — high sensitivity for detecting positive cases  <br>
    • ROC-AUC Score: ~0.98 — excellent class separability  <br>
    • 5-Fold Cross-Validation: Consistent performance with low variance  
  </p>
</div>
""", unsafe_allow_html=True)

#Tech Stack
divider("Tech Stack")

st.markdown("""
<div class="stat-grid">
  <div class="stat-card">
    <div class="val" style="font-size:1.5rem;">🐍</div>
    <div class="lbl">Python 3.12</div>
  </div>
  <div class="stat-card">
    <div class="val" style="font-size:1.5rem;">🎈</div>
    <div class="lbl">Streamlit</div>
  </div>
  <div class="stat-card">
    <div class="val" style="font-size:1.5rem;">🌲</div>
    <div class="lbl">scikit-learn</div>
  </div>
  <div class="stat-card">
    <div class="val" style="font-size:1.5rem;">🐼</div>
    <div class="lbl">Pandas</div>
  </div>
  <div class="stat-card">
    <div class="val" style="font-size:1.5rem;">📈</div>
    <div class="lbl">Matplotlib</div>
  </div>
  <div class="stat-card">
    <div class="val" style="font-size:1.5rem;">🗄️</div>
    <div class="lbl">SQLite</div>
  </div>
</div>
""", unsafe_allow_html=True)

#References
divider("References")

st.markdown("""
<div class="feature-card">
  <h4>📚 References</h4>
  <p>
    1. <strong>World Health Organization (WHO)</strong> — Cardiovascular diseases fact sheet.
    <a href="https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases-(cvds)" target="_blank">who.int</a><br><br>
    2. <strong>UCI Heart Disease Dataset</strong> — Janosi, A., Steinbrunn, W., Pfisterer, M., &amp; Detrano, R. (1988).
    Heart Disease. UCI Machine Learning Repository.
    <a href="https://archive.ics.uci.edu/dataset/45/heart+disease" target="_blank">archive.ics.uci.edu</a><br><br>
    3. <strong>Pedregosa et al. (2011)</strong> — Scikit-learn: Machine Learning in Python.
    <em>Journal of Machine Learning Research</em>, 12, 2825–2830.<br><br>
    4. <strong>Géron, A. (2019)</strong> — <em>Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow</em>
    (2nd ed.). O'Reilly Media.
  </p>
</div>
""", unsafe_allow_html=True)

#Disclaimer
st.markdown("""
<div class="disclaimer">
  ⚕️ <strong>Medical Disclaimer:</strong> CardioScan is developed for educational
  and research purposes only. It is not a substitute for professional medical advice,
  diagnosis, or treatment. Always consult a qualified healthcare professional.
</div>
""", unsafe_allow_html=True)
