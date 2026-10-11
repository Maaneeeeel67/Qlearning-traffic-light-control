# fichier: training.py
import numpy as np
import os
import matplotlib.pyplot as plt
from simulation.carrefour import Carrefour
from agents.q_learning_agent import QLearningAgent
import config

def smooth(data, window=25):
    """Calcule la moyenne mobile pour lisser les courbes."""
    if len(data) < window:
        return data
    return np.convolve(data, np.ones(window)/window, mode='valid')

def entrainement(scenario, nom_scenario="equilibre"):
    print(f"\n--- Début de l'entraînement : {nom_scenario} ---")
    
    env = Carrefour(taux_arrivees=scenario, duree_orange=config.DUREE_ORANGE)
    agent = QLearningAgent(
        alpha=config.ALPHA, 
        gamma=config.GAMMA, 
        epsilon_start=config.EPSILON_START,
        epsilon_end=config.EPSILON_END,
        epsilon_decay=config.EPSILON_DECAY
    )
    
    recompenses_episodes = []
    epsilons = []
    
    for episode in range(1, config.EPISODES + 1):
        etat = env.reset()
        recompense_cumulee = 0
        
        for pas in range(config.PAS_PAR_EPISODE):
            action = agent.choisir_action(etat)
            prochain_etat, recompense = env.step(action)
            
            agent.apprendre(etat, action, recompense, prochain_etat)
            
            etat = prochain_etat
            recompense_cumulee += recompense
            
        agent.decroitre_epsilon()
        recompenses_episodes.append(recompense_cumulee)
        epsilons.append(agent.epsilon)
        
        if episode % 50 == 0:
            print(f"Épisode {episode}/{config.EPISODES} | Récompense: {recompense_cumulee:.1f} | Epsilon: {agent.epsilon:.3f}")

    # Sauvegarde du modèle
    model_path = os.path.join(config.MODELS_DIR, f"q_table_{nom_scenario}.npy")
    agent.sauvegarder(model_path)
    
    # Visualisation de la convergence
    plt.figure(figsize=(12, 6))
    plt.plot(recompenses_episodes, alpha=0.3, label="Brut", color="blue")
    plt.plot(range(len(smooth(recompenses_episodes))), smooth(recompenses_episodes), label="Lissé (Moyenne mobile)", color="red", linewidth=2)
    plt.title(f"Convergence du Q-Learning - Scénario {nom_scenario}")
    plt.xlabel("Épisodes")
    plt.ylabel("Récompense cumulée")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plot_path = os.path.join(config.RESULTS_DIR, f"convergence_{nom_scenario}.png")
    plt.savefig(plot_path)
    plt.close()
    
    return recompenses_episodes, epsilons

if __name__ == "__main__":
    entrainement(config.SCENARIO_EQUILIBRE, "equilibre")
