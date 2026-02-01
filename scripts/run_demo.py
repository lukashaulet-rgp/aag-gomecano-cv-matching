"""
Script de démonstration du matching Gomécanicien.
Charge les profils extraits et les compare au besoin opérationnel.
"""
import os
import sys

# Ajoute le dossier src au chemin de recherche de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from aag.scoring.scorer import calculate_match, rank_candidates
from aag.utils.io import load_json


def load_all_profiles(json_dir="data/samples_json/"):
    """Charge tous les profils JSON du dossier."""
    profils = []

    if not os.path.exists(json_dir):
        print(f"Erreur: Le dossier {json_dir} n'existe pas.")
        return profils

    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(json_dir, filename)
            try:
                profil = load_json(filepath)
                profils.append(profil)
            except Exception as e:
                print(f"Erreur lors du chargement de {filename}: {e}")

    return profils


def display_ranking(results, besoin):
    """Affiche le classement de manière lisible."""

    print("\n" + "=" * 70)
    print("CLASSEMENT DES CANDIDATS")
    print("=" * 70)

    for i, res in enumerate(results, 1):
        # Indicateur de recommandation
        if res["score"] >= 80:
            status = "RECOMMANDE"
        elif res["score"] >= 50:
            status = "A CONSIDERER"
        else:
            status = "NON PRIORITAIRE"

        print(f"\n{'-' * 70}")
        print(f"#{i} | {res['nom']} | SCORE: {res['score']}/100 | {status}")
        print(f"{'-' * 70}")
        print(f"   Ville: {res['ville']} | Experience: {res['experience']} ans")
        print(f"   Competences: {', '.join(res['competences'])}")
        print(f"   Justification:")
        for j in res["justifications"]:
            print(f"      - {j}")


def run_matching_demo():
    """Fonction principale de démonstration."""

    print("\n" + "=" * 70)
    print("ASSISTANT D'ACQUISITION GOMECANICIEN - DEMO MATCHING")
    print("=" * 70)

    # 1. Charger le besoin
    besoin_path = "data/besoin.json"
    if not os.path.exists(besoin_path):
        print(f"Erreur: Fichier {besoin_path} introuvable.")
        return

    besoin = load_json(besoin_path)

    print(f"\n--- BESOIN OPERATIONNEL ---")
    print(f"Mission: {besoin.get('id_mission', 'N/A')}")
    print(f"Zone: {besoin.get('ville_cible', 'N/A')}")
    print(f"Competence requise: {besoin.get('competence_requise', 'N/A')}")
    print(f"Experience minimum: {besoin.get('experience_min', 0)} ans")
    print(f"Type: {besoin.get('type_mission', 'N/A')}")
    print(f"Urgence: {besoin.get('urgence', 'N/A')}")

    # 2. Charger les profils
    profils = load_all_profiles()

    if not profils:
        print("\nAucun profil trouve dans data/samples_json/")
        print("Lancez d'abord: python scripts/run_ingestion.py")
        return

    print(f"\n{len(profils)} profil(s) charge(s) pour analyse.")

    # 3. Calculer le matching
    results = rank_candidates(profils, besoin)

    # 4. Afficher le classement
    display_ranking(results, besoin)

    # 5. Résumé pour le COMEX
    print("\n" + "=" * 70)
    print("RESUME POUR DECISION")
    print("=" * 70)

    top_candidate = results[0] if results else None
    if top_candidate and top_candidate["score"] >= 50:
        print(f"\nRECOMMANDATION: Contacter {top_candidate['nom']} en priorite.")
        print(f"Score de compatibilite: {top_candidate['score']}%")
    else:
        print("\nAUCUN CANDIDAT ne correspond parfaitement au besoin.")
        print("Suggestion: Elargir la zone de recherche ou ajuster les criteres.")


if __name__ == "__main__":
    run_matching_demo()
