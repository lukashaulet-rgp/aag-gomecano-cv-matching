"""
Interface graphique Streamlit - Assistant d'Acquisition Gomecanicien
Jour 4 : Dashboard de matching candidats / missions B2B
"""
import os
import sys
import json

# Ajoute le dossier src au chemin Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
from aag.scoring.scorer import calculate_match, rank_candidates
from aag.utils.io import load_json


# =============================================================================
# CONFIGURATION DE LA PAGE
# =============================================================================
st.set_page_config(
    page_title="AAG - Gomecano Matching",
    page_icon="🔧",
    layout="wide"
)


# =============================================================================
# CHARGEMENT DES DONNEES
# =============================================================================
@st.cache_data
def load_profiles(json_dir="data/samples_json/"):
    """Charge tous les profils JSON disponibles."""
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
    """Charge le besoin par defaut."""
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
# SIDEBAR - CONFIGURATION DU BESOIN
# =============================================================================
st.sidebar.title("Configuration Mission")

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
st.sidebar.subheader("Poids des criteres")

poids_ville = st.sidebar.slider("Poids Ville", 0, 100, besoin_defaut.get("poids_ville", 50))
poids_competence = st.sidebar.slider("Poids Competence", 0, 100, besoin_defaut.get("poids_competence", 30))
poids_experience = st.sidebar.slider("Poids Experience", 0, 100, besoin_defaut.get("poids_experience", 20))

total_poids = poids_ville + poids_competence + poids_experience
if total_poids != 100:
    st.sidebar.warning(f"Total des poids : {total_poids}/100")
else:
    st.sidebar.success("Total des poids : 100/100")

# Construction du besoin
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
st.title("Assistant d'Acquisition Gomecanicien")
st.markdown("**Matching intelligent entre missions B2B et profils mecaniciens**")

# Chargement des profils
profils = load_profiles()

if not profils:
    st.error("Aucun profil trouve dans `data/samples_json/`. Lancez d'abord `python scripts/run_ingestion.py`.")
    st.stop()

# Resume du besoin
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Mission", id_mission)
col2.metric("Zone", ville_cible)
col3.metric("Competence", competence_requise)
col4.metric("Exp. minimum", f"{experience_min} ans")

# =============================================================================
# RESULTATS DU MATCHING
# =============================================================================
st.markdown("---")
st.subheader("Classement des candidats")

results = rank_candidates(profils, besoin)

for i, res in enumerate(results):
    score = res["score"]

    # Couleur selon le score
    if score >= 80:
        status = "RECOMMANDE"
        color = "green"
    elif score >= 50:
        status = "A CONSIDERER"
        color = "orange"
    else:
        status = "NON PRIORITAIRE"
        color = "red"

    with st.container():
        col_rank, col_info, col_score = st.columns([1, 4, 2])

        with col_rank:
            st.markdown(f"### #{i + 1}")

        with col_info:
            st.markdown(f"**{res['nom']}**")
            st.caption(f"{res['ville']} | {res['experience']} ans | {', '.join(res['competences'])}")

        with col_score:
            st.markdown(f"### :{color}[{score}/100]")
            st.caption(status)

        # Justifications dans un expander
        with st.expander(f"Details du scoring - {res['nom']}"):
            for j in res["justifications"]:
                st.markdown(f"- {j}")

        st.markdown("---")

# =============================================================================
# RESUME POUR LE COMEX
# =============================================================================
st.subheader("Resume pour decision")

top = results[0] if results else None

if top and top["score"] >= 50:
    st.success(f"**RECOMMANDATION** : Contacter **{top['nom']}** en priorite (score {top['score']}%)")

    # Tableau comparatif
    import pandas as pd
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

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption(f"AAG Gomecano - {len(profils)} profil(s) analyses | Poids: Ville {poids_ville}% / Competence {poids_competence}% / Experience {poids_experience}%")
