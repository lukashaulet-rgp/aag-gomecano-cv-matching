"""
Moteur de scoring pour le matching Gomécanicien / Mission.
Calcule un score de compatibilité et génère une justification lisible.
"""
from .rules import get_experience_category, get_bonus_competences, is_priority_city


def calculate_match(profil, besoin):
    """
    Calcule le score de compatibilité entre un profil et un besoin.

    Args:
        profil: Dictionnaire du profil Gomécanicien (extrait du JSON)
        besoin: Dictionnaire du besoin opérationnel

    Returns:
        Tuple (score, liste_justifications)
        - score: Note sur 100 (peut dépasser 100 avec les bonus)
        - justifications: Liste de strings expliquant le score
    """
    score = 0
    justifications = []

    # Récupération des données du profil
    ville_profil = profil.get("ville", "Inconnue")
    competences = profil.get("competences", [])
    experience = profil.get("experience_annees", 0)

    # Récupération des critères du besoin
    ville_cible = besoin.get("ville_cible", "")
    competence_requise = besoin.get("competence_requise", "")
    experience_min = besoin.get("experience_min", 0)

    # Poids des critères
    poids_ville = besoin.get("poids_ville", 50)
    poids_competence = besoin.get("poids_competence", 30)
    poids_experience = besoin.get("poids_experience", 20)

    # =========================================================================
    # 1. CRITÈRE GÉOGRAPHIQUE (Crucial pour la mobilité)
    # =========================================================================
    if ville_profil.lower() == ville_cible.lower():
        score += poids_ville
        justifications.append(f"Localisation parfaite ({ville_profil})")
    elif is_priority_city(ville_profil):
        # Bonus partiel si dans une ville prioritaire proche
        score += poids_ville * 0.5
        justifications.append(f"Zone PACA ({ville_profil})")
    else:
        justifications.append(f"Hors zone cible ({ville_profil})")

    # =========================================================================
    # 2. CRITÈRE COMPÉTENCE TECHNIQUE
    # =========================================================================
    if competence_requise in competences:
        score += poids_competence
        justifications.append(f"Expert en {competence_requise}")
    else:
        # Vérifier si d'autres compétences pertinentes
        if competences:
            score += poids_competence * 0.3
            justifications.append(f"Autres compétences: {', '.join(competences[:2])}")
        else:
            justifications.append(f"Compétence {competence_requise} non validée")

    # =========================================================================
    # 3. CRITÈRE EXPÉRIENCE
    # =========================================================================
    category = get_experience_category(experience)

    if experience >= experience_min:
        score += poids_experience
        justifications.append(f"Expérience confirmée ({experience} ans - {category})")
    elif experience > 0:
        # Score proportionnel à l'expérience
        ratio = experience / experience_min
        score += poids_experience * ratio
        justifications.append(f"Profil {category} ({experience} ans)")
    else:
        justifications.append("Expérience non renseignée")

    # =========================================================================
    # 4. BONUS STRATÉGIQUES (VUL, Électrique, etc.)
    # =========================================================================
    bonus, bonus_details = get_bonus_competences(competences)
    if bonus > 0:
        score += bonus
        justifications.append(f"Bonus compétences: {', '.join(bonus_details)}")

    return round(score, 1), justifications


def rank_candidates(profils, besoin):
    """
    Classe une liste de profils selon leur compatibilité avec un besoin.

    Args:
        profils: Liste de dictionnaires profils
        besoin: Dictionnaire du besoin

    Returns:
        Liste triée par score décroissant avec détails
    """
    results = []

    for profil in profils:
        score, justifications = calculate_match(profil, besoin)

        results.append({
            "nom": profil.get("nom", "Inconnu"),
            "fichier": profil.get("fichier_source", ""),
            "score": score,
            "justifications": justifications,
            "ville": profil.get("ville", ""),
            "experience": profil.get("experience_annees", 0),
            "competences": profil.get("competences", [])
        })

    # Tri par score décroissant
    results.sort(key=lambda x: x["score"], reverse=True)

    return results
