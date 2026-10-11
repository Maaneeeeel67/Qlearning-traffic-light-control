# fichier: quick_test.py
import sys
import os

# Ajout du dossier au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import numpy as np
    import matplotlib
    from config import SCENARIO_EQUILIBRE
    from simulation.carrefour import Carrefour
    from agents.q_learning_agent import QLearningAgent
    from agents.baseline_agent import BaselineAgent
    print("✅ Imports réussis.")
except ImportError as e:
    print(f"❌ Erreur d'import : {e}")
    sys.exit(1)

def test_simulation():
    print("Test de la simulation...")
    env = Carrefour(SCENARIO_EQUILIBRE)
    etat = env.reset()
    assert len(etat) == 5, "L'état doit être un tuple de 5 éléments"
    
    # Faire un pas
    prochain_etat, recompense = env.step(1) # Changer de phase
    assert env.orange_restant > 0, "L'orange devrait être actif après un changement"
    print("✅ Simulation fonctionnelle.")

def test_agent():
    print("Test de l'agent...")
    agent = QLearningAgent()
    etat = (1, 1, 1, 1, 0)
    action = agent.choisir_action(etat)
    agent.apprendre(etat, action, -10, (1, 1, 1, 1, 1))
    assert etat in agent.Q, "L'état devrait être dans la Q-table après apprentissage"
    print("✅ Agent Q-Learning fonctionnel.")

if __name__ == "__main__":
    print("--- Test Rapide de l'Installation ---")
    test_simulation()
    test_agent()
    print("\nTout semble OK ! Vous pouvez lancer l'entraînement avec :")
    print("python main.py --train --scenario equilibre")
