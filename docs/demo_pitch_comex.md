# Script de Demo - Pitch COMEX

## Contexte
Ce document est le guide de presentation du POC AAG (Assistant d'Acquisition Gomecanicien) devant le Comite Executif de Gomecano.

## Probleme actuel
- Les CV de mecaniciens arrivent en PDF non structures
- Le tri est 100% manuel par les recruteurs
- Temps moyen de qualification : 15-20 min par CV
- Risque d'erreur humaine sur les criteres techniques

## Solution proposee : AAG
Un assistant intelligent qui :
1. **Lit** automatiquement les CV PDF
2. **Extrait** les donnees cles (nom, ville, competences, experience)
3. **Compare** chaque profil au besoin operationnel
4. **Classe** les candidats avec un score de compatibilite
5. **Explique** chaque decision (transparence IA)

## Deroulement de la demo

### Etape 1 : Montrer le besoin (30 sec)
> "Imaginons une mission urgente : nous cherchons un mecanicien a Marseille, specialise en electrique, avec minimum 3 ans d'experience."

Ouvrir `data/besoin.json` et montrer les parametres.

### Etape 2 : Lancer le matching (30 sec)
> "Le systeme analyse automatiquement tous les CV disponibles."

```bash
python scripts/run_demo.py
```

Montrer le classement avec les scores et justifications.

### Etape 3 : Interface interactive (2 min)
> "Le recruteur peut ajuster les criteres en temps reel."

```bash
streamlit run src/app_streamlit.py
```

Demontrer :
- Changer la ville cible
- Modifier les poids des criteres
- Observer le classement qui se met a jour

### Etape 4 : Transparence (1 min)
> "Chaque recommandation est justifiee. Le systeme explique pourquoi tel candidat est classe premier."

Ouvrir le detail du scoring du candidat #1, montrer les justifications.

## Chiffres cles a presenter
| Metrique | Avant | Avec AAG |
|----------|-------|----------|
| Temps de tri par CV | 15-20 min | < 1 sec |
| Criteres evalues | Variable | 3 standardises + bonus |
| Transparence | Aucune | Justification complete |
| Biais humain | Possible | Elimine |

## Prochaines etapes (si POC valide)
1. Connexion a une base de donnees de CV
2. Enrichissement des regles metier avec l'equipe RH
3. Integration avec le CRM Gomecano
4. Ajout de criteres (disponibilite, certifications, mobilite)

## Questions anticipees du COMEX

**"Est-ce que l'IA remplace le recruteur ?"**
> Non. L'IA pre-qualifie et classe. Le recruteur valide la recommandation finale.

**"Comment on ajoute de nouveaux criteres ?"**
> Il suffit d'enrichir le fichier `rules.py` avec de nouveaux mots-cles ou bonus.

**"C'est fiable ?"**
> Le systeme est testable et transparent. Chaque score est decompose et justifie.
