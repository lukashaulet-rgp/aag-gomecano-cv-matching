"""
Script principal d'ingestion des CV.
Lit tous les PDF du dossier samples_cvs et génère les profils JSON.
"""
import os
import sys

# Ajoute le dossier src au chemin de recherche de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from aag.ingestion.extractor import run_extraction_pipeline
from aag.utils.io import save_json


def main():
    """Point d'entrée principal du script d'ingestion."""

    # Dossiers de travail
    input_dir = "data/samples_cvs/"

    # Vérifie que le dossier existe
    if not os.path.exists(input_dir):
        print(f"Erreur: Le dossier {input_dir} n'existe pas.")
        return

    # Liste tous les fichiers PDF
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"Aucun CV trouvé dans {input_dir}. Ajoutez des fichiers PDF pour tester.")
        return

    print(f"{'='*60}")
    print(f"INGESTION DES CV - {len(pdf_files)} fichier(s) trouvé(s)")
    print(f"{'='*60}\n")

    # Compteurs
    success_count = 0
    profiles = []

    # Traitement de chaque CV
    for filename in pdf_files:
        pdf_path = os.path.join(input_dir, filename)

        print(f"\n--- Traitement: {filename} ---")

        # Extraction du profil
        profile = run_extraction_pipeline(pdf_path)

        if profile:
            # Ajoute le nom du fichier source
            profile["fichier_source"] = filename

            # Génère un nom de fichier JSON
            json_filename = filename.replace(".pdf", ".json").replace(".PDF", ".json")

            # Sauvegarde en JSON
            save_json(profile, json_filename)

            profiles.append(profile)
            success_count += 1

    # Résumé final
    print(f"\n{'='*60}")
    print(f"RÉSUMÉ DE L'INGESTION")
    print(f"{'='*60}")
    print(f"Fichiers traités: {len(pdf_files)}")
    print(f"Extractions réussies: {success_count}")
    print(f"Fichiers JSON générés dans: data/samples_json/")

    # Affiche un aperçu des profils extraits
    if profiles:
        print(f"\n--- APERÇU DES PROFILS ---")
        for p in profiles:
            print(f"  • {p['nom']} | {p['ville']} | {p['experience_annees']} ans | {p['competences']}")


if __name__ == "__main__":
    main()
