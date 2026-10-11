# fichier: simulation/carrefour.py
import numpy as np
import random
from config import SEUILS_DISCRETISATION, DIRECTIONS

class Carrefour:
    def __init__(self, taux_arrivees, duree_orange=2):
        """
        taux_arrivees: dict {'N': val, 'S': val, 'E': val, 'O': val}
        duree_orange: nb de pas pendant lesquels le trafic est bloqué lors d'un changement
        """
        self.taux_arrivees = taux_arrivees
        self.duree_orange_config = duree_orange
        self.reset()

    def reset(self):
        """Réinitialise l'état du carrefour."""
        self.files = {d: 0 for d in DIRECTIONS}
        self.phase = 0  # 0: Nord-Sud vert, 1: Est-Ouest vert
        self.orange_restant = 0
        return self._get_state()

    def _arrivees_poisson(self, lambda_val):
        """Génère un nombre de véhicules selon une loi de Poisson."""
        return np.random.poisson(lambda_val / 60.0) # Normalisé par pas de temps (simulé)

    def _ajouter_arrivees(self):
        """Ajoute des véhicules sur chaque file d'attente."""
        for d in DIRECTIONS:
            nouveau = self._arrivees_poisson(self.taux_arrivees[d])
            self.files[d] += nouveau

    def _ecouler_vehicules(self):
        """Fait sortir des véhicules selon la phase active (si pas en orange)."""
        if self.orange_restant > 0:
            return # Pas d'écoulement pendant l'orange

        if self.phase == 0: # Nord-Sud
            self.files["N"] = max(0, self.files["N"] - 1)
            self.files["S"] = max(0, self.files["S"] - 1)
        else: # Est-Ouest
            self.files["E"] = max(0, self.files["E"] - 1)
            self.files["O"] = max(0, self.files["O"] - 1)

    def _discretiser(self, valeur):
        """Convertit le nombre de véhicules en un niveau discret (0-4)."""
        for i, seuil in enumerate(reversed(SEUILS_DISCRETISATION)):
            if valeur >= seuil:
                return len(SEUILS_DISCRETISATION) - 1 - i
        return 0

    def _get_state(self):
        """Retourne l'état actuel sous forme de tuple (qN, qS, qE, qO, phase)."""
        return (
            self._discretiser(self.files["N"]),
            self._discretiser(self.files["S"]),
            self._discretiser(self.files["E"]),
            self._discretiser(self.files["O"]),
            self.phase
        )

    def _calculer_recompense(self):
        """La récompense est le négatif de la somme des véhicules en attente."""
        return -sum(self.files.values())

    def step(self, action):
        """
        Exécute un pas de temps.
        Action: 0 = Garder la phase, 1 = Changer de phase
        """
        recompense_cumulee = 0
        
        # Gestion du changement de phase
        if action == 1 and self.orange_restant == 0:
            self.orange_restant = self.duree_orange_config
            # On change la phase immédiatement en interne pour la logique d'affichage 
            # mais l'écoulement attendra la fin de l'orange.
            self.phase = 1 - self.phase
        
        # Un pas de temps
        self._ajouter_arrivees()
        self._ecouler_vehicules()
        
        if self.orange_restant > 0:
            self.orange_restant -= 1
            
        recompense = self._calculer_recompense()
        prochain_etat = self._get_state()
        
        return prochain_etat, recompense
