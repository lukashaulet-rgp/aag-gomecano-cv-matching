🏗️ Architecture de l'Assistant d'Acquisition Gomécano (AAG)
Ce document décrit le fonctionnement technique du POC développé pour Gomécano.

1. Vision d'ensemble
L'objectif est de transformer des candidatures non structurées (PDF) en fiches de profils exploitables pour le recrutement de mécaniciens mobiles.

2. Le Pipeline de Données
Le flux de données suit trois étapes clés :

Ingestion (src/aag/ingestion/) :

Lecture des fichiers PDF bruts.

Conversion en texte (String Python).

Analyse & Structuration (src/aag/scoring/) :

Recherche de mots-clés (Compétences, Ville, Expérience).

Mapping vers un modèle de données JSON standardisé.

Aide à la Décision (app_streamlit.py) :

Comparaison du profil avec un "Besoin Client" (ex: Mission B2B à Marseille).

Calcul d'un score de compatibilité de 0 à 100%.

3. Composants Techniques
Langage : Python 3.1x

Parsing : PyPDF2 (Léger et rapide, sans dépendances lourdes).

Interface : Streamlit (Pour une présentation interactive COMEX).

Stockage : Fichiers JSON (Pas de base de données complexe pour le POC).

4. Modèle de Données (Target)
Chaque Gomécanicien est représenté par cet objet :

nom : Identité

ville : Zone d'intervention

skills : Liste de compétences techniques (Freinage, Elec, etc.)

seniority : Nombre d'années d'expérience

## 5. Arborescence du Projet

```
aag-gomecano-cv-matching/
├── data/
│   ├── samples_cvs/        # CV PDF de test
│   ├── samples_json/       # Profils extraits (sortie)
│   └── besoin.json         # Définition d'un besoin opérationnel
├── docs/
│   ├── architecture.md     # Ce fichier
│   ├── demo_pitch_comex.md # Script de présentation
│   └── scoring_rules.md    # Règles de scoring
├── scripts/
│   ├── run_ingestion.py    # Point d'entrée extraction
│   └── run_demo.py         # Lancement démo
├── src/
│   ├── aag/
│   │   ├── ingestion/      # Lecture PDF + nettoyage
│   │   ├── models/         # Structures de données
│   │   ├── scoring/        # Logique de matching
│   │   └── utils/          # Helpers (IO, logs)
│   └── app_streamlit.py    # Interface web
└── tests/                  # Tests unitaires
```

## 6. Check-list de Validation - Jour 1

- [x] Arborescence complète créée
- [x] 3 CV PDF de test dans `data/samples_cvs/`
- [x] Script `run_ingestion.py` fonctionnel
- [x] Fichier `architecture.md` documenté
- [ ] Premier commit Git effectué