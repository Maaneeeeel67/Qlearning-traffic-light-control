# fichier: agents/baseline_agent.py

class BaselineAgent:
    def __init__(self, duree_phase=30):
        """
        Agent à cycles fixes.
        duree_phase: temps en pas de temps avant de changer de phase.
        """
        self.duree_phase = duree_phase
        self.compteur = 0

    def choisir_action(self, etat):
        """
        Retourne 1 (changer) si le compteur atteint le seuil, sinon 0.
        Note: On ne change que si on n'est pas déjà en train de changer 
        (géré par l'environnement, mais ici on suit le compteur).
        """
        self.compteur += 1
        if self.compteur >= self.duree_phase:
            self.compteur = 0
            return 1 # Changer
        return 0 # Garder
    
    def reset(self):
        self.compteur = 0
