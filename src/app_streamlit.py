"""
Interface graphique Streamlit - Assistant d'Acquisition Gomecanicien
Dashboard de matching candidats / missions B2B
"""
import os
import sys

# Ajoute le dossier src au chemin Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from aag.scoring.scorer import calculate_match, rank_candidates
from aag.utils.io import load_json


# =============================================================================
# COULEURS
# =============================================================================
C = {
    "primary": "#4F46E5",       # Indigo
    "primary_light": "#818CF8",
    "primary_bg": "#EEF2FF",
    "success": "#059669",       # Vert emeraude
    "success_bg": "#ECFDF5",
    "warning": "#D97706",       # Ambre
    "warning_bg": "#FFFBEB",
    "danger": "#DC2626",        # Rouge
    "danger_bg": "#FEF2F2",
    "text": "#111827",          # Quasi-noir
    "text_secondary": "#6B7280",# Gris
    "border": "#E5E7EB",
    "bg_card": "#FFFFFF",
    "bg_page": "#F9FAFB",
}


# =============================================================================
# CONFIGURATION PAGE
# =============================================================================
st.set_page_config(
    page_title="AAG - Gomecano Matching",
    page_icon="https://img.icons8.com/fluency/48/gear.png",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================================================================
# CSS
# =============================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body,
    p, h1, h2, h3, h4, h5, h6,
    span, div, label, input, button, select, textarea,
    .stMarkdown, .stText, .stCaption {{
        font-family: 'Inter', -apple-system, sans-serif;
    }}

    .main .block-container {{
        padding-top: 1.5rem;
        max-width: 1100px;
    }}

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {{
        background: {C["bg_card"]};
        border-right: 1px solid {C["border"]};
    }}
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] [data-baseweb="select"] {{
        border: 1px solid {C["border"]} !important;
        border-radius: 8px !important;
    }}
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
        border: 1px solid {C["border"]} !important;
        border-radius: 8px !important;
        background: {C["bg_card"]} !important;
    }}

    /* ---- Hero ---- */
    .hero {{
        background: linear-gradient(135deg, {C["primary"]} 0%, #7C3AED 100%);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }}
    .hero h1 {{
        color: #fff;
        font-size: 1.65rem;
        font-weight: 800;
        margin: 0 0 0.3rem 0;
    }}
    .hero p {{
        color: rgba(255,255,255,0.85);
        font-size: 0.95rem;
        margin: 0;
    }}

    /* ---- KPIs ---- */
    .kpi-row {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.8rem;
        margin-bottom: 1.8rem;
    }}
    .kpi {{
        background: {C["bg_card"]};
        border: 1px solid {C["border"]};
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
    }}
    .kpi .label {{
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: {C["text_secondary"]};
        font-weight: 600;
        margin-bottom: 0.3rem;
    }}
    .kpi .value {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {C["text"]};
    }}

    /* ---- Section title ---- */
    .stitle {{
        font-size: 1.15rem;
        font-weight: 700;
        color: {C["text"]};
        margin: 1.8rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {C["primary"]};
        display: inline-block;
    }}

    /* ---- Candidate badge tag ---- */
    .ctag {{
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        background: {C["primary_bg"]};
        color: {C["primary"]};
        margin-right: 0.25rem;
        margin-bottom: 0.2rem;
    }}

    /* ---- Score badge ---- */
    .sbadge {{
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 5px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}
    .sbadge.high {{ background: {C["success_bg"]}; color: {C["success"]}; }}
    .sbadge.mid  {{ background: {C["warning_bg"]}; color: {C["warning"]}; }}
    .sbadge.low  {{ background: {C["danger_bg"]}; color: {C["danger"]}; }}

    /* ---- Chart wrapper ---- */
    .chart-wrap {{
        background: {C["bg_card"]};
        border: 1px solid {C["border"]};
        border-radius: 10px;
        padding: 0.8rem;
        margin-top: 0.5rem;
    }}

    /* ---- Stats row ---- */
    .srow {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        margin: 0.8rem 0 1.2rem 0;
    }}
    .sbox {{
        background: {C["bg_card"]};
        border: 1px solid {C["border"]};
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }}
    .sbox .num {{
        font-size: 1.6rem;
        font-weight: 800;
    }}
    .sbox .slabel {{
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: {C["text_secondary"]};
        font-weight: 600;
        margin-top: 0.15rem;
    }}

    /* ---- Reco ---- */
    .reco {{
        background: {C["success_bg"]};
        border: 1px solid #A7F3D0;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin: 0.8rem 0 1.2rem 0;
    }}
    .reco .rtitle {{
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: {C["success"]};
        font-weight: 700;
        margin-bottom: 0.4rem;
    }}
    .reco .rtext {{
        font-size: 0.95rem;
        color: {C["text"]};
    }}
    .reco .rtext strong {{
        color: {C["primary"]};
    }}

    /* ---- Footer ---- */
    .foot {{
        text-align: center;
        padding: 1.2rem 0 0.5rem 0;
        margin-top: 2rem;
        border-top: 1px solid {C["border"]};
        font-size: 0.78rem;
        color: {C["text_secondary"]};
    }}

    /* ---- Streamlit overrides ---- */
    div[data-testid="stExpander"] {{
        border: 1px solid {C["border"]};
        border-radius: 8px;
        background: {C["bg_card"]};
    }}
    #MainMenu {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CHARGEMENT DES DONNEES
# =============================================================================
@st.cache_data
def load_profiles(json_dir="data/samples_json/"):
    profils = []
    if not os.path.exists(json_dir):
        return profils
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(json_dir, filename)
            profil = load_json(filepath)
            profil["fichier_source"] = filename
            profils.append(profil)
    return profils


def load_besoin(path="data/besoin.json"):
    if os.path.exists(path):
        return load_json(path)
    return {
        "id_mission": "B2B-001",
        "ville_cible": "Marseille",
        "competence_requise": "electrique",
        "experience_min": 3,
        "poids_ville": 50,
        "poids_competence": 30,
        "poids_experience": 20
    }


# =============================================================================
# SIDEBAR
# =============================================================================
st.sidebar.markdown(f"""
<div style="text-align:center; padding: 0.8rem 0;">
    <div style="font-size: 1.6rem;">&#9881;</div>
    <div style="font-size: 1rem; font-weight: 800; color: {C['primary']}; letter-spacing: 1px;">GOMECANO</div>
    <div style="font-size: 0.65rem; color: {C['text_secondary']}; letter-spacing: 2px; text-transform: uppercase;">Matching Engine</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("##### Configuration Mission")

besoin_defaut = load_besoin()

id_mission = st.sidebar.text_input("ID Mission", value=besoin_defaut.get("id_mission", "B2B-001"))

ville_cible = st.sidebar.selectbox(
    "Ville cible",
    ["Marseille", "Lyon", "Toulouse", "Aix-En-Provence", "Aubagne", "Vitrolles", "Toulon", "Nice", "Paris", "Bordeaux"],
    index=0
)

competence_requise = st.sidebar.selectbox(
    "Competence requise",
    ["electrique", "moteur", "freinage", "pneus", "climatisation", "carrosserie", "vul"],
    index=0
)

experience_min = st.sidebar.slider("Experience minimum (annees)", 0, 20, besoin_defaut.get("experience_min", 3))

st.sidebar.markdown("---")
st.sidebar.markdown("##### Poids des criteres")

poids_ville = st.sidebar.slider("Poids Ville", 0, 100, besoin_defaut.get("poids_ville", 50))
poids_competence = st.sidebar.slider("Poids Competence", 0, 100, besoin_defaut.get("poids_competence", 30))
poids_experience = st.sidebar.slider("Poids Experience", 0, 100, besoin_defaut.get("poids_experience", 20))

total_poids = poids_ville + poids_competence + poids_experience
if total_poids != 100:
    st.sidebar.warning(f"Total des poids : {total_poids}/100")
else:
    st.sidebar.success(f"Total des poids : 100/100")

besoin = {
    "id_mission": id_mission,
    "ville_cible": ville_cible,
    "competence_requise": competence_requise,
    "experience_min": experience_min,
    "poids_ville": poids_ville,
    "poids_competence": poids_competence,
    "poids_experience": poids_experience
}


# =============================================================================
# CONTENU PRINCIPAL
# =============================================================================

# Hero
st.markdown("""
<div class="hero">
    <h1>Assistant d'Acquisition Gomecanicien</h1>
    <p>Matching intelligent entre missions B2B et profils mecaniciens qualifies</p>
</div>
""", unsafe_allow_html=True)

profils = load_profiles()

if not profils:
    st.error("Aucun profil trouve dans `data/samples_json/`. Lancez d'abord `python scripts/run_ingestion.py`.")
    st.stop()

# KPIs
st.markdown(f"""
<div class="kpi-row">
    <div class="kpi">
        <div class="label">Mission</div>
        <div class="value">{id_mission}</div>
    </div>
    <div class="kpi">
        <div class="label">Zone cible</div>
        <div class="value">{ville_cible}</div>
    </div>
    <div class="kpi">
        <div class="label">Competence</div>
        <div class="value">{competence_requise}</div>
    </div>
    <div class="kpi">
        <div class="label">Exp. minimum</div>
        <div class="value">{experience_min} ans</div>
    </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# CLASSEMENT
# =============================================================================
results = rank_candidates(profils, besoin)

st.markdown('<div class="stitle">Classement des candidats</div>', unsafe_allow_html=True)


def _score_color(score):
    if score >= 80:
        return "green", "high", "RECOMMANDE"
    elif score >= 50:
        return "orange", "mid", "A CONSIDERER"
    return "red", "low", "NON PRIORITAIRE"


for i, res in enumerate(results):
    score = res["score"]
    st_color, cls, label = _score_color(score)

    tags_html = "".join(f'<span class="ctag">{c}</span>' for c in res["competences"])

    col_rank, col_info, col_score = st.columns([0.6, 5, 1.2])

    with col_rank:
        st.markdown(f"**#{i + 1}**")

    with col_info:
        st.markdown(f"**{res['nom']}**")
        st.caption(f"{res['ville']} | {res['experience']} ans d'experience")
        st.markdown(tags_html, unsafe_allow_html=True)

    with col_score:
        st.markdown(f"### :{st_color}[{score}]")
        st.markdown(f'<span class="sbadge {cls}">{label}</span>', unsafe_allow_html=True)

    with st.expander(f"Details du scoring - {res['nom']}"):
        for j in res["justifications"]:
            st.markdown(f"- {j}")

    st.divider()


# =============================================================================
# GRAPHIQUE
# =============================================================================
st.markdown('<div class="stitle">Visualisation des scores</div>', unsafe_allow_html=True)

noms = [r["nom"] for r in reversed(results)]
scores = [r["score"] for r in reversed(results)]
bar_colors = [
    C["success"] if s >= 80 else C["warning"] if s >= 50 else C["danger"]
    for s in scores
]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=scores,
    y=noms,
    orientation="h",
    marker=dict(color=bar_colors, cornerradius=4),
    text=[f" {s}" for s in scores],
    textposition="outside",
    textfont=dict(size=13, color=C["text"], family="Inter, sans-serif"),
    hovertemplate="<b>%{y}</b><br>Score : %{x}/100<extra></extra>",
))

fig.add_vline(
    x=80, line_dash="dot", line_color=C["primary"], line_width=2,
    annotation_text="Seuil 80",
    annotation_position="top",
    annotation_font=dict(color=C["primary"], size=11, family="Inter, sans-serif"),
)

fig.update_layout(
    xaxis_title="Score de matching",
    yaxis_title="",
    xaxis=dict(
        range=[0, 110],
        gridcolor="#E5E7EB",
        tickfont=dict(color=C["text_secondary"], size=11, family="Inter, sans-serif"),
        title_font=dict(color=C["text_secondary"], size=12, family="Inter, sans-serif"),
    ),
    yaxis=dict(
        tickfont=dict(color=C["text"], size=12, family="Inter, sans-serif"),
    ),
    height=max(400, len(results) * 38),
    margin=dict(l=10, r=50, t=35, b=45),
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    hoverlabel=dict(bgcolor="#fff", font_size=13, font_family="Inter, sans-serif", bordercolor=C["border"]),
)

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# RESUME
# =============================================================================
st.markdown('<div class="stitle">Resume pour decision</div>', unsafe_allow_html=True)

top = results[0] if results else None
nb_reco = sum(1 for r in results if r["score"] >= 80)
nb_consider = sum(1 for r in results if 50 <= r["score"] < 80)
nb_low = sum(1 for r in results if r["score"] < 50)

st.markdown(f"""
<div class="srow">
    <div class="sbox">
        <div class="num" style="color:{C['success']}">{nb_reco}</div>
        <div class="slabel">Recommandes</div>
    </div>
    <div class="sbox">
        <div class="num" style="color:{C['warning']}">{nb_consider}</div>
        <div class="slabel">A considerer</div>
    </div>
    <div class="sbox">
        <div class="num" style="color:{C['danger']}">{nb_low}</div>
        <div class="slabel">Non prioritaires</div>
    </div>
</div>
""", unsafe_allow_html=True)

if top and top["score"] >= 50:
    st.markdown(f"""
    <div class="reco">
        <div class="rtitle">Recommandation principale</div>
        <div class="rtext">Contacter <strong>{top['nom']}</strong> en priorite &mdash; score de compatibilite de <strong>{top['score']}%</strong></div>
    </div>
    """, unsafe_allow_html=True)

    df = pd.DataFrame([
        {
            "Rang": i + 1,
            "Nom": r["nom"],
            "Ville": r["ville"],
            "Experience": f"{r['experience']} ans",
            "Score": f"{r['score']}/100"
        }
        for i, r in enumerate(results)
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.warning("Aucun candidat ne correspond au besoin. Ajustez les criteres dans la barre laterale.")

# Footer
st.markdown(f"""
<div class="foot">
    <strong>AAG Gomecano</strong> &middot; {len(profils)} profil(s) analyses &middot;
    Poids : Ville {poids_ville}% / Competence {poids_competence}% / Experience {poids_experience}%
</div>
""", unsafe_allow_html=True)
