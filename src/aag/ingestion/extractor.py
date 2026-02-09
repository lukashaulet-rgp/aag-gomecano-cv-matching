"""
Module d'extraction de profils Gomécanicien.
Transforme le texte brut des CV en données structurées.
"""
import re
from .pdf_reader import read_pdf
from .text_cleaner import clean_text
from aag.utils.logger import logger


# =============================================================================
# DICTIONNAIRES DE RECHERCHE (à enrichir par les étudiants)
# =============================================================================

# Catégories de compétences et leurs mots-clés associés
SKILLS_DB = {
    "moteur": ["moteur", "distribution", "culasse", "embrayage", "vidange", "courroie"],
    "freinage": ["frein", "freinage", "disque", "plaquette", "abs", "étrier"],
    "electrique": ["électrique", "electrique", "batterie", "alternateur", "démarreur",
                   "hybride", "diagnostic", "valise", "injection"],
    "pneus": ["pneu", "pneumatique", "parallélisme", "équilibrage", "géométrie"],
    "climatisation": ["climatisation", "clim", "recharge"],
    "carrosserie": ["carrosserie", "peinture", "débosselage"],
    "vul": ["vul", "utilitaire", "véhicule utilitaire", "flotte"]
}

# Villes cibles pour Gomécano (zone PACA élargie)
VILLES_CIBLES = [
    "marseille", "aix-en-provence", "aix en provence", "aubagne",
    "vitrolles", "cassis", "la ciotat", "martigues", "salon",
    "toulon", "nice", "cannes", "antibes", "avignon",
    "lyon", "toulouse", "paris", "bordeaux", "nantes"
]


def extract_name(text):
    """
    Extrait le nom du candidat (généralement en début de CV).
    Heuristique simple : première ligne en majuscules.
    """
    lines = text.strip().split('\n')
    for line in lines[:5]:  # Chercher dans les 5 premières lignes
        line = line.strip()
        # Si la ligne ressemble à un nom (2-4 mots, majuscules)
        if line and len(line.split()) >= 2 and len(line.split()) <= 4:
            # Vérifier s'il y a des majuscules
            if any(c.isupper() for c in line):
                return line.title()
    return "Nom Inconnu"


def extract_skills(cleaned_text):
    """
    Extrait les compétences trouvées dans le texte.

    Returns:
        Liste des catégories de compétences identifiées
    """
    found_skills = []

    for category, keywords in SKILLS_DB.items():
        for keyword in keywords:
            if keyword in cleaned_text:
                if category not in found_skills:
                    found_skills.append(category)
                break  # Catégorie trouvée, passer à la suivante

    return found_skills


def extract_city(cleaned_text):
    """
    Extrait la ville du candidat.

    Returns:
        Nom de la ville ou "Inconnue"
    """
    for ville in VILLES_CIBLES:
        if ville in cleaned_text:
            return ville.title()
    return "Inconnue"


def extract_experience(cleaned_text):
    """
    Extrait le nombre d'années d'expérience.
    Recherche des patterns comme "X ans", "X années", etc.

    Returns:
        Nombre d'années (int) ou 0 si non trouvé
    """
    # Patterns pour trouver l'expérience
    patterns = [
        r'(\d+)\s*ans?\s*d.exp[ée]rience',  # "5 ans d'expérience"
        r'exp[ée]rience\s*:\s*(\d+)',         # "Expérience: 5"
        r'(\d+)\s*ans?\s*en\s*m[ée]canique',  # "5 ans en mécanique"
        r'(\d+)\s*ann[ée]es?',                # "5 années"
        r'depuis\s*(\d+)\s*ans?',             # "depuis 5 ans"
    ]

    max_years = 0
    for pattern in patterns:
        matches = re.findall(pattern, cleaned_text)
        for match in matches:
            years = int(match)
            if years > max_years and years < 50:  # Sanity check
                max_years = years

    return max_years


def extract_profile_data(raw_text):
    """
    Fonction principale d'extraction.
    Transforme le texte brut en dictionnaire structuré.

    Args:
        raw_text: Texte brut extrait du PDF

    Returns:
        Dictionnaire avec les informations du profil
    """
    if not raw_text:
        return None

    # Nettoyage du texte
    cleaned = clean_text(raw_text)

    # Extraction des différents champs
    profile = {
        "nom": extract_name(raw_text),  # Utilise le texte brut pour garder la casse
        "ville": extract_city(cleaned),
        "competences": extract_skills(cleaned),
        "experience_annees": extract_experience(cleaned),
        "texte_source": cleaned[:500]  # Garde un extrait pour debug
    }

    return profile


def run_extraction_pipeline(pdf_path):
    """
    Pipeline complet : PDF -> Texte -> Profil structuré.

    Args:
        pdf_path: Chemin vers le fichier PDF

    Returns:
        Dictionnaire du profil ou None si erreur
    """
    # 1. Lecture du PDF
    raw_text = read_pdf(pdf_path)

    if not raw_text:
        logger.error(f"Impossible de lire {pdf_path}")
        return None

    # 2. Extraction des données
    profile = extract_profile_data(raw_text)

    if profile:
        logger.info(f"Profil extrait : {profile['nom']} | {profile['ville']} | {profile['experience_annees']} ans | {profile['competences']}")

    return profile
