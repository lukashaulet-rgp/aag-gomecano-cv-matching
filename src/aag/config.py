"""
Configuration centrale du projet AAG Gomecano.
Regroupe tous les chemins et parametres par defaut.
"""
import os

# Repertoire racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Chemins des dossiers de donnees
DATA_DIR = os.path.join(BASE_DIR, "data")
CV_DIR = os.path.join(DATA_DIR, "samples_cvs")
JSON_DIR = os.path.join(DATA_DIR, "samples_json")
BESOIN_PATH = os.path.join(DATA_DIR, "besoin.json")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Parametres de scoring par defaut
DEFAULT_POIDS_VILLE = 50
DEFAULT_POIDS_COMPETENCE = 30
DEFAULT_POIDS_EXPERIENCE = 20
DEFAULT_EXPERIENCE_MIN = 3

# Seuils de recommandation
SEUIL_RECOMMANDE = 80
SEUIL_A_CONSIDERER = 50
