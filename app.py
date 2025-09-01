"""Streamlit Dashboard for SC Riessersee Eishockey Fan Engagement"""

import json
import os
from collections import Counter
from pathlib import Path

import pandas as pd
import streamlit as st

SCR_DUNKELBLAU = "#202A44"
SCR_HELLBLAU = "#009FE3"
SCR_WEISS = "#FFFFFF"


def check_password():
    """Function verifying the password."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if not st.session_state["authenticated"]:
        with st.form("Login"):
            pw = st.text_input("Passwort", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if pw == os.environ.get("SCR_DASHBOARD_PASSWORD", ""):
                    st.session_state["authenticated"] = True
                else:
                    st.error("Falsches Passwort!")
        st.stop()


check_password()

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

logo_path = Path("sc-riessersee-eishockey-logo.svg")
if logo_path.exists():
    st.image(str(logo_path), width=180)

st.title("SC Riessersee Eishockey Fan Dashboard")

st.write("Dashboard für die Digital Customer Journey der Fans des SC Riessersee.")

# Load data
with open("fans_data.json", "r", encoding="utf-8") as f:
    fans = json.load(f)

df = pd.DataFrame(fans)

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Anzahl Fans", len(df))
col2.metric(
    "Ø Recency (Tage)",
    (pd.to_datetime("today") - pd.to_datetime(df["last_contact"]))
    .dt.days.mean()
    .round(0),
)
col3.metric("Ø Frequency (Tage)", df["frequency"].mean().round(0))
col4.metric("Ø Umsatz (€)", df["monetary"].mean().round(0))

# Customer Lifetime Value
with st.container(border=True):
    st.subheader("Customer Lifetime Value (CLV)")
    st.markdown("""
        Der Customer Lifetime Value (CLV) zeigt, wie wertvoll einzelne Fans für den Verein sind. 
        So können gezielt VIP-Angebote oder Treueaktionen entwickelt werden.
    """)
    st.bar_chart(
        df.set_index("name")["clv"].sort_values(ascending=False).head(20),
        color=SCR_HELLBLAU,
    )

# Segmente
with st.container(border=True):
    st.subheader("Fan-Segmente")
    st.markdown(
        """Fan-Segmente helfen, gezielte Kampagnen für verschiedene Gruppen zu erstellen 
        – z.B. Eventbesucher, Online-Shopper oder Social-Media-Fans.
        """
    )
    segments_flat = [seg for seglist in df["segments"] for seg in seglist]
    segment_counts = Counter(segments_flat)
    st.bar_chart(pd.Series(segment_counts), color=SCR_HELLBLAU)

# Touchpoints Visualisierung
with st.container(border=True):
    st.subheader("Touchpoints & Interaktionen"
    st.markdown("""
        Die Übersicht der digitalen Touchpoints zeigt, welche Kanäle am meisten genutzt werden 
        und wo Potenzial für mehr Interaktion liegt.
    """)
    touchpoints = {
        "Social Media Interaktionen": df["social_media_interactions"].sum(),
        "Newsletter Abonnenten": df["newsletter"].sum(),
        "Käufe (Frequency)": df["frequency"].sum(),
    }
    st.bar_chart(pd.Series(touchpoints), color=SCR_HELLBLAU)

# Zufriedenheit
with st.container(border=True):
    st.subheader("Fan-Zufriedenheit")
    st.line_chart(
        df.sort_values("satisfaction")["satisfaction"].reset_index(drop=True),
        color=SCR_HELLBLAU,
    )

# Filter & Detailansicht
with st.container(border=True):
    st.subheader("Fan-Details")
    fan_select = st.selectbox("Wähle einen Fan", df["name"])
    fan_data = df[df["name"] == fan_select].iloc[0]
    st.json(fan_data.to_dict())

st.markdown(
    """
    - [SCR Homepage](https://www.scriessersee.de/)
    - Google Analytics, Ticketshop Eventim, Merchandise Shop Woocommerce, 
    - Social Media Kanäle, Newsletter 
    - Saisonkalender
    """,
)
