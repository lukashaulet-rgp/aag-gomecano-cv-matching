"""
Tests unitaires pour le module d'extraction de profils.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from aag.ingestion.extractor import (
    extract_name,
    extract_skills,
    extract_city,
    extract_experience,
    extract_profile_data
)
from aag.ingestion.text_cleaner import clean_text


class TestCleanText(unittest.TestCase):
    """Tests pour le nettoyage de texte."""

    def test_lowercase(self):
        self.assertEqual(clean_text("HELLO WORLD"), "hello world")

    def test_newlines_removed(self):
        result = clean_text("ligne1\nligne2\nligne3")
        self.assertNotIn("\n", result)

    def test_double_spaces(self):
        result = clean_text("mot1   mot2     mot3")
        self.assertEqual(result, "mot1 mot2 mot3")

    def test_empty_input(self):
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text(None), "")


class TestExtractName(unittest.TestCase):
    """Tests pour l'extraction du nom."""

    def test_nom_simple(self):
        text = "Marc Durand\nMecanicien automobile\nMarseille"
        result = extract_name(text)
        self.assertEqual(result, "Marc Durand")

    def test_nom_inconnu(self):
        text = "a\nb\nc"
        result = extract_name(text)
        self.assertEqual(result, "Nom Inconnu")


class TestExtractSkills(unittest.TestCase):
    """Tests pour l'extraction des competences."""

    def test_competence_electrique(self):
        text = "expert en diagnostic electrique et batterie"
        result = extract_skills(text)
        self.assertIn("electrique", result)

    def test_competence_freinage(self):
        text = "specialiste plaquette de frein et disque"
        result = extract_skills(text)
        self.assertIn("freinage", result)

    def test_competence_vul(self):
        text = "maintenance de flotte utilitaire vul"
        result = extract_skills(text)
        self.assertIn("vul", result)

    def test_aucune_competence(self):
        text = "bonjour je suis disponible"
        result = extract_skills(text)
        self.assertEqual(result, [])

    def test_competences_multiples(self):
        text = "moteur distribution freinage disque batterie electrique"
        result = extract_skills(text)
        self.assertIn("moteur", result)
        self.assertIn("freinage", result)
        self.assertIn("electrique", result)


class TestExtractCity(unittest.TestCase):
    """Tests pour l'extraction de la ville."""

    def test_marseille(self):
        result = extract_city("habite a marseille depuis 5 ans")
        self.assertEqual(result, "Marseille")

    def test_lyon(self):
        result = extract_city("domicile lyon 69000")
        self.assertEqual(result, "Lyon")

    def test_ville_inconnue(self):
        result = extract_city("habite a strasbourg")
        self.assertEqual(result, "Inconnue")


class TestExtractExperience(unittest.TestCase):
    """Tests pour l'extraction de l'experience."""

    def test_experience_standard(self):
        result = extract_experience("12 ans d'experience en mecanique")
        self.assertEqual(result, 12)

    def test_experience_format_court(self):
        result = extract_experience("5 annees dans le domaine")
        self.assertEqual(result, 5)

    def test_pas_experience(self):
        result = extract_experience("debutant sans mention d'annees")
        self.assertEqual(result, 0)


class TestExtractProfileData(unittest.TestCase):
    """Tests pour l'extraction complete d'un profil."""

    def test_profil_complet(self):
        text = "Marc Durand\nMecanicien a Marseille\n10 ans d'experience\nExpert moteur et freinage"
        result = extract_profile_data(text)
        self.assertIsNotNone(result)
        self.assertEqual(result["ville"], "Marseille")
        self.assertIn("moteur", result["competences"])

    def test_texte_vide(self):
        result = extract_profile_data("")
        self.assertIsNone(result)

    def test_texte_none(self):
        result = extract_profile_data(None)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
