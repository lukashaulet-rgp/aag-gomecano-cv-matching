"""
Modele de donnees pour un profil Gomecanicien.
"""


class Profil:
    """Represente un mecanicien candidat extrait d'un CV."""

    def __init__(self, nom, ville, competences=None, experience_annees=0, fichier_source=""):
        self.nom = nom
        self.ville = ville
        self.competences = competences or []
        self.experience_annees = experience_annees
        self.fichier_source = fichier_source

    def to_dict(self):
        """Convertit le profil en dictionnaire (compatible JSON)."""
        return {
            "nom": self.nom,
            "ville": self.ville,
            "competences": self.competences,
            "experience_annees": self.experience_annees,
            "fichier_source": self.fichier_source
        }

    @classmethod
    def from_dict(cls, data):
        """Cree un Profil a partir d'un dictionnaire JSON."""
        return cls(
            nom=data.get("nom", "Inconnu"),
            ville=data.get("ville", "Inconnue"),
            competences=data.get("competences", []),
            experience_annees=data.get("experience_annees", 0),
            fichier_source=data.get("fichier_source", "")
        )

    def has_competence(self, competence):
        """Verifie si le profil possede une competence donnee."""
        return competence in self.competences

    def __repr__(self):
        return f"Profil({self.nom}, {self.ville}, {self.experience_annees}ans, {self.competences})"
