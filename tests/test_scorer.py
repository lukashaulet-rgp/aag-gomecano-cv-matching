"""
Tests unitaires pour le moteur de scoring.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from aag.scoring.scorer import calculate_match, rank_candidates
from aag.scoring.rules import get_experience_category, get_bonus_competences, is_priority_city


# Fixtures de test
BESOIN_MARSEILLE_ELEC = {
    "id_mission": "TEST-001",
    "ville_cible": "Marseille",
    "competence_requise": "electrique",
    "experience_min": 3,
    "poids_ville": 50,
    "poids_competence": 30,
    "poids_experience": 20
}

PROFIL_PARFAIT = {
    "nom": "Marc Expert",
    "ville": "Marseille",
    "competences": ["electrique", "moteur", "vul"],
    "experience_annees": 10
}

PROFIL_MOYEN = {
    "nom": "Jean Moyen",
    "ville": "Lyon",
    "competences": ["electrique", "freinage"],
    "experience_annees": 5
}

PROFIL_FAIBLE = {
    "nom": "Paul Junior",
    "ville": "Paris",
    "competences": ["pneus"],
    "experience_annees": 1
}


class TestRules(unittest.TestCase):
    """Tests pour les regles metier."""

    def test_junior(self):
        self.assertEqual(get_experience_category(1), "junior")
        self.assertEqual(get_experience_category(2), "junior")

    def test_confirme(self):
        self.assertEqual(get_experience_category(3), "confirme")
        self.assertEqual(get_experience_category(5), "confirme")

    def test_senior(self):
        self.assertEqual(get_experience_category(10), "senior")
        self.assertEqual(get_experience_category(15), "senior")

    def test_bonus_vul(self):
        bonus, details = get_bonus_competences(["vul", "moteur"])
        self.assertEqual(bonus, 10)

    def test_bonus_electrique(self):
        bonus, details = get_bonus_competences(["electrique"])
        self.assertEqual(bonus, 5)

    def test_bonus_cumul(self):
        bonus, details = get_bonus_competences(["vul", "electrique", "climatisation"])
        self.assertEqual(bonus, 18)  # 10 + 5 + 3

    def test_pas_de_bonus(self):
        bonus, details = get_bonus_competences(["pneus", "moteur"])
        self.assertEqual(bonus, 0)

    def test_ville_prioritaire(self):
        self.assertTrue(is_priority_city("Marseille"))
        self.assertTrue(is_priority_city("marseille"))
        self.assertTrue(is_priority_city("Aubagne"))

    def test_ville_non_prioritaire(self):
        self.assertFalse(is_priority_city("Paris"))
        self.assertFalse(is_priority_city("Lyon"))


class TestCalculateMatch(unittest.TestCase):
    """Tests pour le calcul de score."""

    def test_profil_parfait_score_eleve(self):
        score, justifications = calculate_match(PROFIL_PARFAIT, BESOIN_MARSEILLE_ELEC)
        self.assertGreaterEqual(score, 80)

    def test_profil_faible_score_bas(self):
        score, justifications = calculate_match(PROFIL_FAIBLE, BESOIN_MARSEILLE_ELEC)
        self.assertLess(score, 50)

    def test_ville_match_donne_points(self):
        score_marseille, _ = calculate_match(PROFIL_PARFAIT, BESOIN_MARSEILLE_ELEC)
        score_lyon, _ = calculate_match(PROFIL_MOYEN, BESOIN_MARSEILLE_ELEC)
        self.assertGreater(score_marseille, score_lyon)

    def test_competence_match_donne_points(self):
        profil_avec = {"nom": "A", "ville": "Paris", "competences": ["electrique"], "experience_annees": 0}
        profil_sans = {"nom": "B", "ville": "Paris", "competences": ["pneus"], "experience_annees": 0}
        score_avec, _ = calculate_match(profil_avec, BESOIN_MARSEILLE_ELEC)
        score_sans, _ = calculate_match(profil_sans, BESOIN_MARSEILLE_ELEC)
        self.assertGreater(score_avec, score_sans)

    def test_experience_suffisante(self):
        profil_senior = {"nom": "A", "ville": "Paris", "competences": [], "experience_annees": 10}
        profil_junior = {"nom": "B", "ville": "Paris", "competences": [], "experience_annees": 1}
        score_senior, _ = calculate_match(profil_senior, BESOIN_MARSEILLE_ELEC)
        score_junior, _ = calculate_match(profil_junior, BESOIN_MARSEILLE_ELEC)
        self.assertGreater(score_senior, score_junior)

    def test_justifications_non_vides(self):
        _, justifications = calculate_match(PROFIL_PARFAIT, BESOIN_MARSEILLE_ELEC)
        self.assertGreater(len(justifications), 0)

    def test_score_arrondi(self):
        score, _ = calculate_match(PROFIL_MOYEN, BESOIN_MARSEILLE_ELEC)
        self.assertEqual(score, round(score, 1))


class TestRankCandidates(unittest.TestCase):
    """Tests pour le classement des candidats."""

    def test_classement_ordre_decroissant(self):
        profils = [PROFIL_FAIBLE, PROFIL_PARFAIT, PROFIL_MOYEN]
        results = rank_candidates(profils, BESOIN_MARSEILLE_ELEC)
        scores = [r["score"] for r in results]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_profil_parfait_en_premier(self):
        profils = [PROFIL_FAIBLE, PROFIL_PARFAIT, PROFIL_MOYEN]
        results = rank_candidates(profils, BESOIN_MARSEILLE_ELEC)
        self.assertEqual(results[0]["nom"], "Marc Expert")

    def test_tous_les_profils_presents(self):
        profils = [PROFIL_FAIBLE, PROFIL_PARFAIT, PROFIL_MOYEN]
        results = rank_candidates(profils, BESOIN_MARSEILLE_ELEC)
        self.assertEqual(len(results), 3)

    def test_liste_vide(self):
        results = rank_candidates([], BESOIN_MARSEILLE_ELEC)
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
