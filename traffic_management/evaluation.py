# fichier: evaluation.py
import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from simulation.carrefour import Carrefour
from agents.q_learning_agent import QLearningAgent
from agents.baseline_agent import BaselineAgent
import config

def evaluer_agent(agent, scenario, episodes=50):
    env = Carrefour(taux_arrivees=scenario, duree_orange=config.DUREE_ORANGE)
    recompenses = []
    
    for _ in range(episodes):
        etat = env.reset()
        if hasattr(agent, 'reset'): agent.reset()
        
        cumul = 0
        for _ in range(config.PAS_PAR_EPISODE):
            # En évaluation, on n'explore pas (epsilon=0) si c'est Q-Learning
            if hasattr(agent, 'epsilon'):
                old_eps = agent.epsilon
                agent.epsilon = 0
                action = agent.choisir_action(etat)
                agent.epsilon = old_eps
            else:
                action = agent.choisir_action(etat)
                
            etat, recompense = env.step(action)
            cumul += recompense
        recompenses.append(cumul)
    
    return np.mean(recompenses), np.std(recompenses)

def comparer(scenario, nom_scenario="equilibre"):
    print(f"\n--- Évaluation du scénario : {nom_scenario} ---")
    
    # 1. Charger l'agent Q-Learning entraîné
    ql_agent = QLearningAgent()
    model_path = os.path.join(config.MODELS_DIR, f"q_table_{nom_scenario}.npy")
    ql_agent.charger(model_path)
    
    # 2. Initialiser l'agent Baseline
    base_agent = BaselineAgent(duree_phase=20) # 20 pas par phase
    
    # 3. Lancer l'évaluation
    score_ql, std_ql = evaluer_agent(ql_agent, scenario)
    score_base, std_base = evaluer_agent(base_agent, scenario)
    
    improvement = ((score_ql - score_base) / abs(score_base)) * 100
    
    print(f"Q-Learning: {score_ql:.2f} (+/- {std_ql:.2f})")
    print(f"Baseline:   {score_base:.2f} (+/- {std_base:.2f})")
    print(f"Amélioration: {improvement:.2f}%")
    
    # 4. Exporter les résultats CSV
    csv_path = os.path.join(config.RESULTS_DIR, f"comparaison_{nom_scenario}.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Agent", "Moyenne", "Ecart-Type"])
        writer.writerow(["Q-Learning", score_ql, std_ql])
        writer.writerow(["Baseline", score_base, std_base])
    
    # 5. Graphique de comparaison
    labels = ['Baseline', 'Q-Learning']
    means = [score_base, score_ql]
    stds = [std_base, std_ql]
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, means, yerr=stds, capsize=10, color=['#ff9999', '#66b3ff'], alpha=0.8)
    plt.title(f"Performance Moyenne - Scénario {nom_scenario}")
    plt.ylabel("Récompense Cumulée Moyenne")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Ajout des valeurs sur les barres
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval - (abs(yval)*0.05), round(yval, 2), va='bottom', ha='center', fontweight='bold')

    plt.savefig(os.path.join(config.RESULTS_DIR, f"comparaison_{nom_scenario}.png"))
    plt.close()

if __name__ == "__main__":
    comparer(config.SCENARIO_EQUILIBRE, "equilibre")
