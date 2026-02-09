"""
Modele de donnees pour un besoin operationnel (mission B2B).
"""


class Besoin:
    """Represente une demande de mission B2B Gomecano."""

    def __init__(self, id_mission, ville_cible, competence_requise,
                 experience_min=0, poids_ville=50, poids_competence=30,
                 poids_experience=20):
        self.id_mission = id_mission
        self.ville_cible = ville_cible
        self.competence_requise = competence_requise
        self.experience_min = experience_min
        self.poids_ville = poids_ville
        self.poids_competence = poids_competence
        self.poids_experience = poids_experience

    def to_dict(self):
        """Convertit le besoin en dictionnaire (compatible JSON)."""
        return {
            "id_mission": self.id_mission,
            "ville_cible": self.ville_cible,
            "competence_requise": self.competence_requise,
            "experience_min": self.experience_min,
            "poids_ville": self.poids_ville,
            "poids_competence": self.poids_competence,
            "poids_experience": self.poids_experience
        }

    @classmethod
    def from_dict(cls, data):
        """Cree un Besoin a partir d'un dictionnaire JSON."""
        return cls(
            id_mission=data.get("id_mission", ""),
            ville_cible=data.get("ville_cible", ""),
            competence_requise=data.get("competence_requise", ""),
            experience_min=data.get("experience_min", 0),
            poids_ville=data.get("poids_ville", 50),
            poids_competence=data.get("poids_competence", 30),
            poids_experience=data.get("poids_experience", 20)
        )

    def total_poids(self):
        """Verifie que le total des poids fait 100."""
        return self.poids_ville + self.poids_competence + self.poids_experience

    def __repr__(self):
        return f"Besoin({self.id_mission}, {self.ville_cible}, {self.competence_requise})"
