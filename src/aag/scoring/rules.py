"""
Règles métier pour le scoring des Gomécaniciens.
Ces règles peuvent être enrichies par l'équipe selon les besoins de Gomécano.
"""

# Bonus spéciaux pour certaines compétences stratégiques
BONUS_COMPETENCES = {
    "vul": 10,           # Véhicules Utilitaires = stratégique pour B2B
    "electrique": 5,     # Marché en croissance
    "climatisation": 3   # Compétence recherchée
}

# Seuils d'expérience pour les catégories
SEUILS_EXPERIENCE = {
    "junior": 2,      # 0-2 ans
    "confirme": 5,    # 3-5 ans
    "senior": 10      # 6+ ans
}

# Villes prioritaires pour Gomécano (zone PACA)
VILLES_PRIORITAIRES = [
    "marseille",
    "aix-en-provence",
    "aubagne",
    "vitrolles"
]


def get_experience_category(years):
    """
    Retourne la catégorie d'expérience du mécanicien.

    Args:
        years: Nombre d'années d'expérience

    Returns:
        Catégorie: "junior", "confirme" ou "senior"
    """
    if years <= SEUILS_EXPERIENCE["junior"]:
        return "junior"
    elif years <= SEUILS_EXPERIENCE["confirme"]:
        return "confirme"
    else:
        return "senior"


def get_bonus_competences(competences):
    """
    Calcule le bonus total pour les compétences stratégiques.

    Args:
        competences: Liste des compétences du profil

    Returns:
        Tuple (bonus_total, liste_des_bonus_appliqués)
    """
    bonus_total = 0
    bonus_details = []

    for comp in competences:
        if comp in BONUS_COMPETENCES:
            bonus = BONUS_COMPETENCES[comp]
            bonus_total += bonus
            bonus_details.append(f"+{bonus} ({comp})")

    return bonus_total, bonus_details


def is_priority_city(ville):
    """
    Vérifie si la ville est dans la zone prioritaire.

    Args:
        ville: Nom de la ville

    Returns:
        Boolean
    """
    return ville.lower() in VILLES_PRIORITAIRES
