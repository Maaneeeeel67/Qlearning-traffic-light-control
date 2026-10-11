# fichier: agents/q_learning_agent.py
import numpy as np
import random
from collections import defaultdict
import os

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        
        # Q-Table : clé = état (tuple), valeur = liste [Q(s, action0), Q(s, action1)]
        self.Q = defaultdict(lambda: [0.0, 0.0])

    def choisir_action(self, etat):
        """Choisit une action selon la stratégie epsilon-greedy."""
        if random.random() < self.epsilon:
            return random.randint(0, 1) # Exploration
        else:
            return np.argmax(self.Q[etat]) # Exploitation

    def apprendre(self, etat, action, recompense, prochain_etat):
        """Mise à jour de la Q-Table selon la formule du Q-Learning."""
        meilleur_q_suivant = max(self.Q[prochain_etat])
        cible = recompense + self.gamma * meilleur_q_suivant
        # Mise à jour
        self.Q[etat][action] += self.alpha * (cible - self.Q[etat][action])

    def decroitre_epsilon(self):
        """Décroissance exponentielle d'epsilon."""
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)

    def sauvegarder(self, fichier):
        """Sauvegarde la Q-table dans un fichier .npy"""
        # Conversion du defaultdict en dict classique pour numpy
        dict_to_save = dict(self.Q)
        np.save(fichier, dict_to_save)
        print(f"Agent sauvegardé dans {fichier}")

    def charger(self, fichier):
        """Charge la Q-table depuis un fichier .npy"""
        if os.path.exists(fichier):
            loaded_dict = np.load(fichier, allow_pickle=True).item()
            self.Q = defaultdict(lambda: [0.0, 0.0], loaded_dict)
            print(f"Agent chargé depuis {fichier}")
        else:
            print(f"Fichier {fichier} introuvable. Agent initialisé à zéro.")
