import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --red:    #C0392B;
        --red-lt: #E74C3C;
        --red-bg: #FDF1F0;
        --ink:    #1A1A2E;
        --ink-60: #5C5C7A;
        --white:  #FFFFFF;
        --border: #E8D5D3;
        --card:   #FFFAFA;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(145deg, #FDF1F0 0%, #FFF5F5 50%, #FDF8F8 100%);
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }

    [data-testid="stHeader"] { background: transparent; }
    footer { visibility: hidden; }

    /* ── Sidebar nav ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1A2E 0%, #2C1810 100%) !important;
        border-right: 1px solid #3D2020;
    }
    [data-testid="stSidebar"] * { color: #F0E6E6 !important; }
    [data-testid="stSidebar"] .stRadio label {
        font-size: .92rem !important;
        padding: .3rem 0 !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
    }
    [data-testid="stSidebarNav"] a {
        font-family: 'DM Sans', sans-serif !important;
        font-size: .95rem !important;
        color: #F0E6E6 !important;
        border-radius: 8px !important;
        padding: .45rem .8rem !important;
        transition: background .15s;
    }
    [data-testid="stSidebarNav"] a:hover,
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(192,57,43,.35) !important;
        color: #fff !important;
    }
    .sidebar-logo {
        text-align: center;
        padding: 1.4rem 0 1rem;
        border-bottom: 1px solid rgba(255,255,255,.1);
        margin-bottom: .5rem;
    }
    .sidebar-logo span { font-size: 2.4rem; display: block; }
    .sidebar-logo h2 {
        font-family: 'DM Serif Display', serif;
        font-size: 1.3rem;
        margin: .3rem 0 0;
        color: #fff !important;
    }
    .sidebar-logo p {
        font-size: .75rem;
        color: rgba(240,230,230,.55) !important;
        margin: .2rem 0 0;
    }

    /* ── Page hero ── */
    .hero {
        text-align: center;
        padding: 2rem 0 1.2rem;
    }
    .hero-icon {
        font-size: 2.8rem;
        display: block;
        margin-bottom: .4rem;
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1);    opacity: 1;   }
        50%       { transform: scale(1.08); opacity: .85; }
    }
    .hero h1 {
        font-family: 'DM Serif Display', serif;
        font-size: 2.4rem;
        letter-spacing: -.5px;
        margin: 0 0 .3rem;
        color: var(--ink);
    }
    .hero h1 span { color: var(--red); }
    .hero p {
        font-size: .9rem;
        color: var(--ink-60);
        font-weight: 300;
        margin: 0;
    }

    /* ── Divider ── */
    .divider {
        display: flex;
        align-items: center;
        gap: .75rem;
        margin: 1.5rem 0 1.1rem;
    }
    .divider span {
        font-family: 'DM Serif Display', serif;
        font-size: 1.05rem;
        color: var(--red);
        white-space: nowrap;
    }
    .divider::before, .divider::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    /* ── Inputs ── */
    [data-testid="stNumberInput"] input {
        border-radius: 8px !important;
        border: 1.5px solid var(--border) !important;
        background: var(--white) !important;
        color: var(--ink) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: .9rem !important;
        transition: border-color .2s;
    }
    [data-testid="stNumberInput"] input:focus {
        border-color: var(--red) !important;
        box-shadow: 0 0 0 3px rgba(192,57,43,.12) !important;
    }
    [data-testid="stNumberInput"] button {
        background: #fff !important;
        border: 1.5px solid var(--border) !important;
        color: var(--ink) !important;
        border-radius: 8px !important;
    }
    [data-testid="stTextInput"] input {
    border-radius: 12px !important;
    border: 1.5px solid #E8D5D3 !important;
    background: #FFFFFF !important;
    color: #1A1A2E !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 0.9rem !important;
    transition: all 0.25s ease;
}

[data-testid="stTextInput"] input:focus {
    border-color: #C0392B !important;
    box-shadow: 0 0 0 3px rgba(192,57,43,0.12) !important;
}
    [data-testid="stNumberInput"] button:hover {
        background: var(--red-bg) !important;
        border-color: var(--red) !important;
    }
    [data-testid="stNumberInput"] button svg {
        fill: var(--ink) !important;
        stroke: var(--ink) !important;
    }
    [data-testid="stSelectbox"] > div > div {
        border-radius: 8px !important;
        border: 1.5px solid var(--border) !important;
        background: var(--white) !important;
        color: var(--ink) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: .9rem !important;
    }
    label, .stSelectbox label, .stNumberInput label {
        font-size: .82rem !important;
        font-weight: 500 !important;
        color: var(--ink-60) !important;
        text-transform: uppercase !important;
        letter-spacing: .5px !important;
    }

    /* ── Predict button ── */
    [data-testid="stButton"] > button {
        width: 100%;
        padding: .85rem 0;
        background: linear-gradient(135deg, var(--red) 0%, var(--red-lt) 100%);
        color: #fff;
        border: none;
        border-radius: 10px;
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: .4px;
        cursor: pointer;
        transition: opacity .2s, transform .1s;
        margin-top: .5rem;
    }
    [data-testid="stButton"] > button:hover {
        opacity: .9;
        transform: translateY(-1px);
    }

    /* ── Result cards ── */
    .result-card {
        border-radius: 14px;
        padding: 1.6rem 1.8rem;
        margin-top: 1.4rem;
        display: flex;
        align-items: flex-start;
        gap: 1.1rem;
        animation: slideUp .4s ease;
    }
    @keyframes slideUp {
        from { opacity:0; transform: translateY(14px); }
        to   { opacity:1; transform: translateY(0);    }
    }
    .result-card.danger {
        background: linear-gradient(135deg, #FDEDEC 0%, #FDFBFB 100%);
        border: 1.5px solid #E9967A;
    }
    .result-card.safe {
        background: linear-gradient(135deg, #EAFAF1 0%, #FDFDFB 100%);
        border: 1.5px solid #82C99F;
    }
    .result-card .icon { font-size: 2.2rem; line-height: 1; }
    .result-card .content h3 {
        font-family: 'DM Serif Display', serif;
        font-size: 1.35rem;
        margin: 0 0 .3rem;
    }
    .result-card.danger .content h3 { color: #A93226; }
    .result-card.safe   .content h3 { color: #1E8449; }
    .result-card .content p {
        margin: 0;
        font-size: .88rem;
        color: var(--ink-60);
        line-height: 1.55;
    }

    /* ── Probability bar ── */
    .prob-row { margin-top: 1rem; padding: 0 .1rem; }
    .prob-label {
        display: flex;
        justify-content: space-between;
        font-size: .82rem;
        color: var(--ink-60);
        margin-bottom: .35rem;
        font-weight: 500;
    }
    .prob-track {
        height: 8px;
        background: var(--border);
        border-radius: 99px;
        overflow: hidden;
    }
    .prob-fill { height: 100%; border-radius: 99px; transition: width .6s ease; }
    .prob-fill.danger { background: linear-gradient(90deg, var(--red), var(--red-lt)); }
    .prob-fill.safe   { background: linear-gradient(90deg, #27AE60, #58D68D); }

    /* ── Stat cards (used on Evaluation + About pages) ── */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: .9rem;
        margin: 1rem 0;
    }
    .stat-card {
        background: var(--white);
        border: 1.5px solid var(--border);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        text-align: center;
    }
    .stat-card .val {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        color: var(--red);
        line-height: 1;
    }
    .stat-card .lbl {
        font-size: .75rem;
        color: var(--ink-60);
        text-transform: uppercase;
        letter-spacing: .5px;
        margin-top: .3rem;
    }

    /* ── Info / disclaimer box ── */
    .disclaimer {
        margin-top: 1.6rem;
        padding: .9rem 1.1rem;
        background: #FFF9F0;
        border-left: 3px solid #F39C12;
        border-radius: 6px;
        font-size: .8rem;
        color: var(--ink-60);
        line-height: 1.5;
    }
    .info-box {
        padding: 1rem 1.2rem;
        background: #F0F4FF;
        border-left: 3px solid #5B8CFF;
        border-radius: 6px;
        font-size: .85rem;
        color: #2F3F6E;
        line-height: 1.55;
        margin: .8rem 0;
    }

    /* ── History table ── */
    .history-empty {
        margin-top: 1rem;
        padding: 1.1rem 1.3rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #FFF7F6 0%, #FFFFFF 100%);
        border: 1.5px solid #E8D5D3;
        color: #7A7A8C;
        font-size: .9rem;
        text-align: center;
    }
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1.5px solid #E8D5D3;
        background: #FFFFFF !important;
    }
    [data-testid="stDataFrame"] thead { background: linear-gradient(135deg, #C0392B 0%, #E74C3C 100%); }
    [data-testid="stDataFrame"] th {
        color: white !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: .75rem;
        letter-spacing: .5px;
    }
    [data-testid="stDataFrame"] td { color: #2F2F44 !important; font-size: .85rem; }
    [data-testid="stDataFrame"] tbody tr:nth-child(even) { background: #FFF9F8 !important; }
    [data-testid="stDataFrame"] tbody tr:hover { background: #FDEDEC !important; }

    .st-emotion-cache-seewz2 p, .st-emotion-cache-seewz2 ol, .st-emotion-cache-seewz2 ul, .st-emotion-cache-seewz2 dl, .st-emotion-cache-seewz2 li {
    font-size: inherit;
    color: black;
}



    /* ── About page feature cards ── */
    .feature-card {
        background: var(--white);
        border: 1.5px solid var(--border);
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin-bottom: .8rem;
    }
    .feature-card h4 {
        font-family: 'DM Serif Display', serif;
        font-size: 1.05rem;
        color: var(--red);
        margin: 0 0 .3rem;
    }
    .feature-card p {
        font-size: .85rem;
        color: var(--ink-60);
        margin: 0;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)


def sidebar_logo():
    """Renders the CardioScan logo block inside the sidebar."""
    st.sidebar.markdown("""
    <div class="sidebar-logo">
      <span>🫀</span>
      <h2>CardioScan</h2>
      <p>Heart Disease Predictor</p>
    </div>
    """, unsafe_allow_html=True)


def divider(label):
    st.markdown(f'<div class="divider"><span>{label}</span></div>', unsafe_allow_html=True)
