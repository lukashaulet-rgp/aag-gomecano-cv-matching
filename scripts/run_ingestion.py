import os
import sys

# Ajoute le dossier src au chemin de recherche de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from aag.ingestion.extractor import run_extraction_pipeline

def main():
    sample_dir = "data/samples_cvs/"
    files = [f for f in os.listdir(sample_dir) if f.endswith(".pdf")]
    
    if not files:
        print("Aucun CV trouvé dans data/samples_cvs/. Ajoutez un PDF pour tester.")
        return

    for file in files:
        path = os.path.join(sample_dir, file)
        text = run_extraction_pipeline(path)
        print(f"--- Début texte {file} ---\n{text[:200]}...\n")

if __name__ == "__main__":
    main()