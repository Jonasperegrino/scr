import streamlit as st
import json
import pandas as pd
from collections import Counter
from pathlib import Path
import os


SCR_DUNKELBLAU = "#202A44"
SCR_HELLBLAU = "#009FE3"
SCR_WEISS = "#FFFFFF"


def check_password():
    PASSWORD = os.environ.get("SCR_DASHBOARD_PASSWORD", "")
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if not st.session_state["authenticated"]:
        with st.form("Login"):
            pw = st.text_input("Passwort", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if pw == PASSWORD:
                    st.session_state["authenticated"] = True
                else:
                    st.error("Falsches Passwort!")
        st.stop()


check_password()

# Set dashboard background and center logo via CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {SCR_DUNKELBLAU};
    }}
    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        background: {SCR_DUNKELBLAU};
        padding: 2rem 0 1rem 0;
    }}
    h1, h2, h3, h4, h5, h6, .st-emotion-cache-10trblm, .st-emotion-cache-1v0mbdj {{
        color: {SCR_WEISS} !important;
    }}
    .stMetric-value, .stMetric-label {{
        color: {SCR_WEISS} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Centered logo
logo_path = Path("sc-riessersee-eishockey-logo.svg")
if logo_path.exists():
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(str(logo_path), width=180)
    st.markdown("</div>", unsafe_allow_html=True)

st.title("SC Riessersee Fan Dashboard")

st.markdown(
    f"""
    <span style="color:{SCR_WEISS}; font-size:1.1rem;">
    Dashboard für die Digital Customer Journey der Fans des SC Riessersee.
    </span>
    """,
    unsafe_allow_html=True,
)

# Load data
with open("fans_data.json", "r") as f:
    fans = json.load(f)

df = pd.DataFrame(fans)

# Add custom CSS for chart containers
st.markdown(
    """
    <style>
    .chart-container {
        background: #22305a;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.15);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .summary-text {
        color: #fff;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Anzahl Fans", len(df))
col2.metric(
    "Ø Recency (Tage)",
    (pd.to_datetime("today") - pd.to_datetime(df["last_contact"]))
    .dt.days.mean()
    .round(1),
)
col3.metric("Ø Frequency (Tage)", df["frequency"].mean().round(1))
col4.metric("Ø Umsatz (€)", df["monetary"].mean().round(2))

# Customer Lifetime Value
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown(
    '<div class="summary-text">Der Customer Lifetime Value (CLV) zeigt, wie wertvoll einzelne Fans für den Verein sind. So können gezielt VIP-Angebote oder Treueaktionen entwickelt werden.</div>',
    unsafe_allow_html=True,
)
st.subheader("Customer Lifetime Value (CLV)")
st.bar_chart(
    df.set_index("name")["clv"].sort_values(ascending=False).head(20),
    color=SCR_HELLBLAU,
)
st.markdown("</div>", unsafe_allow_html=True)
st.subheader("Customer Lifetime Value (CLV)")
st.bar_chart(
    df.set_index("name")["clv"].sort_values(ascending=False).head(20),
    color=SCR_HELLBLAU,
)
st.markdown("</div>", unsafe_allow_html=True)

# Segmente
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown(
    '<div class="summary-text">Fan-Segmente helfen, gezielte Kampagnen für verschiedene Gruppen zu erstellen – z.B. Eventbesucher, Online-Shopper oder Social-Media-Fans.</div>',
    unsafe_allow_html=True,
)
st.subheader("Fan-Segmente")
segments_flat = [seg for seglist in df["segments"] for seg in seglist]
segment_counts = Counter(segments_flat)
st.bar_chart(pd.Series(segment_counts), color=SCR_HELLBLAU)
st.markdown("</div>", unsafe_allow_html=True)

# Touchpoints Visualisierung
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown(
    '<div class="summary-text">Die Übersicht der digitalen Touchpoints zeigt, welche Kanäle am meisten genutzt werden und wo Potenzial für mehr Interaktion liegt.</div>',
    unsafe_allow_html=True,
)
st.subheader("Touchpoints & Interaktionen")
touchpoints = {
    "Social Media Interaktionen": df["social_media_interactions"].sum(),
    "Newsletter Abonnenten": df["newsletter"].sum(),
    "Käufe (Frequency)": df["frequency"].sum(),
}
st.bar_chart(pd.Series(touchpoints), color=SCR_HELLBLAU)
st.markdown("</div>", unsafe_allow_html=True)

# Zufriedenheit
st.subheader("Fan-Zufriedenheit")
st.line_chart(
    df.sort_values("satisfaction")["satisfaction"].reset_index(drop=True),
    color=SCR_HELLBLAU,
)

# Filter & Detailansicht
st.subheader("Fan-Details")
fan_select = st.selectbox("Wähle einen Fan", df["name"])
fan_data = df[df["name"] == fan_select].iloc[0]
st.json(fan_data.to_dict())

# Segment-Filter
st.subheader("Segment-Analyse")
segment_filter = st.multiselect("Segment auswählen", options=segment_counts.keys())
if segment_filter:
    mask = df["segments"].apply(lambda segs: any(s in segs for s in segment_filter))
    st.dataframe(df[mask].reset_index(drop=True))

st.markdown(
    f"""
    ---
    <span style="color:{SCR_WEISS}; font-size:0.95rem;">
    <b>Quellen:</b><br>
    - <a href="https://www.scriessersee.de/" style="color:{SCR_HELLBLAU};" target="_blank">SCR Homepage</a><br>
    - Google Analytics, Ticketshop Eventim, Merchandise Shop Woocommerce, Social Media, Newsletter, Saisonkalender
    </span>
    """,
    unsafe_allow_html=True,
)
