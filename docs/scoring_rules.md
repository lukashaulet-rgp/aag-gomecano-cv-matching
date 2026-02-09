# Regles de Scoring - AAG Gomecano

## Principe
Le moteur de scoring attribue une note sur 100 a chaque candidat en comparant son profil au besoin operationnel. Le score est decompose en 3 criteres ponderes + des bonus strategiques.

## Criteres principaux

### 1. Localisation geographique (par defaut : 50 pts)
| Situation | Points |
|-----------|--------|
| Ville identique au besoin | 100% du poids |
| Ville dans la zone PACA prioritaire | 50% du poids |
| Hors zone | 0 pts |

**Villes prioritaires PACA** : Marseille, Aix-en-Provence, Aubagne, Vitrolles

### 2. Competence technique (par defaut : 30 pts)
| Situation | Points |
|-----------|--------|
| Competence requise trouvee dans le profil | 100% du poids |
| Autres competences presentes | 30% du poids |
| Aucune competence identifiee | 0 pts |

**Competences reconnues** : moteur, freinage, electrique, pneus, climatisation, carrosserie, vul

### 3. Experience (par defaut : 20 pts)
| Situation | Points |
|-----------|--------|
| Experience >= minimum requis | 100% du poids |
| Experience partielle (> 0 ans) | Proportionnel (experience / minimum) |
| Experience non renseignee | 0 pts |

**Categories** :
- Junior : 0-2 ans
- Confirme : 3-5 ans
- Senior : 6+ ans

## Bonus strategiques
Ces bonus s'ajoutent au score de base et peuvent depasser 100.

| Competence | Bonus | Justification |
|------------|-------|---------------|
| VUL (Vehicule Utilitaire) | +10 pts | Strategique pour le B2B Gomecano |
| Electrique | +5 pts | Marche en forte croissance |
| Climatisation | +3 pts | Competence recherchee |

## Seuils de recommandation
| Score | Statut |
|-------|--------|
| >= 80 | RECOMMANDE |
| >= 50 | A CONSIDERER |
| < 50 | NON PRIORITAIRE |

## Poids personnalisables
Les poids des 3 criteres sont configurables dans `data/besoin.json` ou via l'interface Streamlit. Le total doit faire 100.

Exemple par defaut :
```json
{
    "poids_ville": 50,
    "poids_competence": 30,
    "poids_experience": 20
}
```
