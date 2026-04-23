import streamlit as st
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.metrics import (
    confusion_matrix, classification_report,
    roc_auc_score, roc_curve
)
from sklearn.model_selection import cross_val_score
from utils.styles import inject_css, sidebar_logo, divider

st.set_page_config(
    page_title="CardioScan · Evaluation",
    page_icon="📊",
    layout="centered",
)

inject_css()
sidebar_logo()

#  Page header 
st.markdown("""
<div class="hero">
  <span style="font-size:2.6rem; display:block; margin-bottom:.4rem;">📊</span>
  <h1>Model <span>Evaluation</span></h1>
  <p>Performance metrics for the Random Forest classifier</p>
</div>
""", unsafe_allow_html=True)

# Load model, scaler, and dataset
@st.cache_resource
def load_artifacts():
    with open("heart_disease_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

@st.cache_data
def load_and_prepare_data():
    """Re-creates the exact same X_test and y_test used during training."""
    df = pd.read_csv("Data/heart-uci.csv")

    # Drop unnecessary columns
    df = df.drop(columns=["id", "dataset"])

    # Binarise target: 0 = no disease, 1 = disease
    df["num"] = df["num"].apply(lambda x: 1 if x > 0 else 0)

    # Fill missing values exactly as done in notebook
    num_cols = ["age", "trestbps", "chol", "thalch", "oldpeak", "ca"]
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    cat_cols = ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal"]
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # One-hot encode
    encoded_df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    X = encoded_df.drop("num", axis=1)
    y = encoded_df["num"]

    # Same split as training (random_state=42, stratify=y, test_size=0.2)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale numerical columns
    from sklearn.preprocessing import StandardScaler
    scaler_local = StandardScaler()
    X_train[num_cols] = scaler_local.fit_transform(X_train[num_cols])
    X_test[num_cols]  = scaler_local.transform(X_test[num_cols])

    return X_train, X_test, y_train, y_test, X, y

model, scaler = load_artifacts()

try:
    X_train, X_test, y_train, y_test, X_full, y_full = load_and_prepare_data()
    data_loaded = True
except Exception as e:
    data_loaded = False
    st.error(f"Could not load dataset: {e}. Make sure `Data/heart-uci.csv` is in your project folder.")

if data_loaded:

    # Compute all metrics 
    y_pred  = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    accuracy  = round((y_pred == y_test).mean() * 100, 1)
    roc_auc   = round(roc_auc_score(y_test, y_proba) * 100, 1)
    report    = classification_report(y_test, y_pred, output_dict=True)
    precision = round(report["1"]["precision"] * 100, 1)
    recall    = round(report["1"]["recall"] * 100, 1)
    f1        = round(report["1"]["f1-score"] * 100, 1)
    cv_scores = cross_val_score(model, X_full, y_full, cv=5, scoring="accuracy")
    cv_mean   = round(cv_scores.mean() * 100, 1)
    cv_std    = round(cv_scores.std() * 100, 1)

    #Summary stat cards
    divider("Key Metrics")
    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card">
        <div class="val">{accuracy}%</div>
        <div class="lbl">Accuracy</div>
      </div>
      <div class="stat-card">
        <div class="val">{roc_auc}%</div>
        <div class="lbl">ROC-AUC</div>
      </div>
      <div class="stat-card">
        <div class="val">{precision}%</div>
        <div class="lbl">Precision</div>
      </div>
      <div class="stat-card">
        <div class="val">{recall}%</div>
        <div class="lbl">Recall</div>
      </div>
      <div class="stat-card">
        <div class="val">{f1}%</div>
        <div class="lbl">F1 Score</div>
      </div>
      <div class="stat-card">
        <div class="val">{cv_mean}%</div>
        <div class="lbl">CV Score (5-fold)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-box">
      📐 <strong>Cross-Validation:</strong> {cv_mean}% ± {cv_std}% across 5 folds —
      confirms the model generalises well and isn't overfitting to the test split.
    </div>
    """, unsafe_allow_html=True)

    # Confusion Matrix
    divider("Confusion Matrix")

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor("#FFFAFA")
    ax.set_facecolor("#FFFAFA")

    im = ax.imshow(cm, cmap="RdYlGn", vmin=0)

    # Annotate each cell
    labels = [[f"TN\n{tn}", f"FP\n{fp}"], [f"FN\n{fn}", f"TP\n{tp}"]]
    for i in range(2):
        for j in range(2):
            ax.text(j, i, labels[i][j],
                    ha="center", va="center",
                    fontsize=14, fontweight="bold",
                    color="#1A1A2E",
                    fontfamily="DejaVu Sans")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Predicted\nNo Disease", "Predicted\nDisease"], fontsize=9)
    ax.set_yticklabels(["Actual\nNo Disease", "Actual\nDisease"], fontsize=9)
    ax.set_title("Confusion Matrix", fontsize=12, pad=12, color="#1A1A2E")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown(f"""
    <div class="info-box">
      ✅ <strong>True Positives (TP):</strong> {tp} — correctly predicted heart disease<br>
      ✅ <strong>True Negatives (TN):</strong> {tn} — correctly predicted no disease<br>
      ❌ <strong>False Positives (FP):</strong> {fp} — predicted disease, actually healthy<br>
      ❌ <strong>False Negatives (FN):</strong> {fn} — missed actual disease cases
    </div>
    """, unsafe_allow_html=True)

    # ROC Curve 
    divider("ROC Curve")

    fpr, tpr, _ = roc_curve(y_test, y_proba)

    fig2, ax2 = plt.subplots(figsize=(6, 4.5))
    fig2.patch.set_facecolor("#FFFAFA")
    ax2.set_facecolor("#FFFAFA")

    ax2.plot(fpr, tpr, color="#C0392B", lw=2.5,
             label=f"Random Forest (AUC = {roc_auc/100:.2f})")
    ax2.plot([0, 1], [0, 1], color="#AAAAAA", lw=1.2,
             linestyle="--", label="Random Classifier")
    ax2.fill_between(fpr, tpr, alpha=0.08, color="#C0392B")

    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1.02])
    ax2.set_xlabel("False Positive Rate", fontsize=10, color="#5C5C7A")
    ax2.set_ylabel("True Positive Rate", fontsize=10, color="#5C5C7A")
    ax2.set_title("ROC Curve", fontsize=12, color="#1A1A2E", pad=12)
    ax2.legend(loc="lower right", fontsize=9)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

    # Feature Importance 
    divider("Feature Importance")

    importances = model.feature_importances_
    feat_df = pd.DataFrame({
        "Feature":    X_test.columns,
        "Importance": importances
    }).sort_values("Importance", ascending=True).tail(12)  

    fig3, ax3 = plt.subplots(figsize=(6, 5))
    fig3.patch.set_facecolor("#FFFAFA")
    ax3.set_facecolor("#FFFAFA")

    colours = ["#E74C3C" if v >= feat_df["Importance"].quantile(.75)
               else "#F1948A" if v >= feat_df["Importance"].quantile(.5)
               else "#FADBD8"
               for v in feat_df["Importance"]]

    bars = ax3.barh(feat_df["Feature"], feat_df["Importance"],
                    color=colours, edgecolor="none", height=0.6)

    ax3.set_xlabel("Importance Score", fontsize=9, color="#5C5C7A")
    ax3.set_title("Top Feature Importances (Random Forest)", fontsize=11,
                  color="#1A1A2E", pad=10)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.tick_params(labelsize=8)

    high  = mpatches.Patch(color="#E74C3C", label="High importance")
    med   = mpatches.Patch(color="#F1948A", label="Medium")
    low   = mpatches.Patch(color="#FADBD8", label="Lower")
    ax3.legend(handles=[high, med, low], fontsize=8, loc="lower right")

    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()

    st.markdown("""
    <div class="disclaimer">
      ℹ️ Metrics are computed on the held-out test set (20% of 920 samples = 184 rows),
      using the same random seed and preprocessing as the original training notebook.
    </div>
    """, unsafe_allow_html=True)
