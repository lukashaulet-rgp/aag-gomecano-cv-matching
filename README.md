# AAG - Assistant d'Acquisition Gomecanicien

POC de matching intelligent entre des CV de mecaniciens (PDF) et des missions B2B pour Gomecano.

Le systeme lit automatiquement les CV, extrait les donnees cles, et classe les candidats par score de compatibilite avec une mission donnee.

## Fonctionnalites

- **Ingestion PDF** : Lecture et extraction automatique des CV (nom, ville, competences, experience)
- **Moteur de scoring** : Calcul de compatibilite sur 100 avec 3 criteres ponderes + bonus strategiques
- **Justification IA** : Chaque score est decompose et explique
- **Interface Streamlit** : Dashboard interactif pour ajuster les criteres en temps reel
- **40 tests unitaires** : Couverture complete de l'extracteur et du scorer

## Architecture

```
aag-gomecano-cv-matching/
├── data/
│   ├── samples_cvs/        # CV PDF de test
│   ├── samples_json/       # Profils extraits (sortie)
│   └── besoin.json         # Besoin operationnel configurable
├── docs/
│   ├── architecture.md     # Architecture technique
│   ├── scoring_rules.md    # Regles de scoring detaillees
│   └── demo_pitch_comex.md # Guide de presentation COMEX
├── scripts/
│   ├── run_ingestion.py    # Pipeline d'extraction PDF -> JSON
│   └── run_demo.py         # Demo matching en terminal
├── src/
│   ├── aag/
│   │   ├── ingestion/      # pdf_reader, text_cleaner, extractor
│   │   ├── models/         # Classes Profil et Besoin
│   │   ├── scoring/        # scorer, rules
│   │   ├── utils/          # io, logger
│   │   └── config.py       # Configuration centrale
│   └── app_streamlit.py    # Interface web
└── tests/                  # Tests unitaires
```

## Installation

```bash
git clone https://github.com/lukashaulet-rgp/aag-gomecano-cv-matching.git
cd aag-gomecano-cv-matching
pip install PyPDF2 streamlit
```

## Utilisation

```bash
# 1. Extraire les CV en JSON
python scripts/run_ingestion.py

# 2. Lancer le matching en terminal
python scripts/run_demo.py

# 3. Lancer l'interface graphique
streamlit run src/app_streamlit.py

# 4. Lancer les tests
python -m unittest discover tests/ -v
```

## Scoring

Le score de compatibilite est calcule sur 3 criteres :

| Critere | Poids par defaut | Description |
|---------|-----------------|-------------|
| Ville | 50 pts | Match geographique avec la zone cible |
| Competence | 30 pts | Presence de la competence requise |
| Experience | 20 pts | Nombre d'annees vs minimum requis |

Bonus strategiques : VUL (+10), Electrique (+5), Climatisation (+3)

## Stack technique

- **Python 3.12**
- **PyPDF2** - Lecture des PDF
- **Streamlit** - Interface web interactive
- **unittest** - Tests unitaires
