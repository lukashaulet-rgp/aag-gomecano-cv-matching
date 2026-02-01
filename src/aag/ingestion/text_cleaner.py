"""
Module de nettoyage de texte pour les CV.
Transforme le texte brut en texte propre pour l'analyse.
"""
import re


def clean_text(text):
    """
    Nettoie le texte pour faciliter la recherche de mots-clés.

    Args:
        text: Texte brut extrait du PDF

    Returns:
        Texte nettoyé en minuscules, sans caractères spéciaux excessifs
    """
    if not text:
        return ""

    # Tout en minuscules
    text = text.lower()

    # Remplace les retours à la ligne par des espaces
    text = text.replace('\n', ' ')

    # Supprime les doubles espaces et plus
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
