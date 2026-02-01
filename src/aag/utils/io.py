"""
Module utilitaire pour les opérations d'entrée/sortie.
Gère la sauvegarde et le chargement des fichiers JSON.
"""
import json
import os


def save_json(data, filename, output_dir="data/samples_json"):
    """
    Sauvegarde un dictionnaire Python en fichier JSON.

    Args:
        data: Dictionnaire à sauvegarder
        filename: Nom du fichier (ex: "profil_marc.json")
        output_dir: Dossier de destination
    """
    # Créer le dossier s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Profil sauvegardé : {path}")


def load_json(filepath):
    """
    Charge un fichier JSON en dictionnaire Python.

    Args:
        filepath: Chemin complet vers le fichier JSON

    Returns:
        Dictionnaire Python
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
