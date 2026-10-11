# fichier: visualisation.py
import numpy as np
import matplotlib.pyplot as plt
import os
import config
from simulation.carrefour import Carrefour
from agents.q_learning_agent import QLearningAgent

def plot_epsilon_decay(epsilons, fichier_sortie):
    plt.figure(figsize=(8, 4))
    plt.plot(epsilons, color='green')
    plt.title("Décroissance d'Epsilon (Exploration)")
    plt.xlabel("Épisodes")
    plt.ylabel("Epsilon")
    plt.grid(True)
    plt.savefig(fichier_sortie)
    plt.close()

def plot_etats_visites(q_table, fichier_sortie):
    """
    Affiche une approximation des états visités à partir de la Q-table.
    Comme l'état est multidimensionnel, on projette sur (Somme files, Phase).
    """
    if not q_table:
        return
        
    counts = np.zeros((20, 2)) # Somme de 0 à 19 (discrétisé), Phase 0 ou 1
    for etat, values in q_table.items():
        if any(v != 0.0 for v in values):
            somme_files = sum(etat[:4])
            phase = etat[4]
            if somme_files < 20:
                counts[int(somme_files), int(phase)] += 1
                
    plt.figure(figsize=(10, 8))
    plt.imshow(counts.T, aspect='auto', cmap='YlOrRd', origin='lower')
    plt.colorbar(label='Nombre d\'entrées Q-table actives')
    plt.title("Heatmap des États Visités (Projetée)")
    plt.xlabel("Intensité cumulée du trafic (Somme des niveaux)")
    plt.ylabel("Phase active (0: NS, 1: EO)")
    plt.savefig(fichier_sortie)
    plt.close()

def animation_temps_reel(scenario, agent_path, duree=150):
    """La simulation parfaite : Dashboard + Schéma interactif du carrefour."""
    env = Carrefour(taux_arrivees=scenario, duree_orange=config.DUREE_ORANGE)
    agent = QLearningAgent()
    agent.charger(agent_path)
    agent.epsilon = 0 
    
    etat = env.reset()
    history = {d: [] for d in config.DIRECTIONS}
    
    plt.ioff()
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, height_ratios=[2, 1])
    
    ax_map = fig.add_subplot(gs[0, 0])   # Vue schématique du carrefour
    ax_main = fig.add_subplot(gs[0, 1])  # Historique des files
    ax_bars = fig.add_subplot(gs[1, :])   # Statut détaillé

    print("Lancement de la simulation parfaite... (Appuyez sur Ctrl+C pour quitter)")
    
    try:
        for t in range(duree):
            action = agent.choisir_action(etat)
            etat, _ = env.step(action)
            for d in config.DIRECTIONS: history[d].append(env.files[d])
            
            # --- 1. VUE SCHÉMATIQUE (MAP) ---
            ax_map.clear()
            ax_map.set_xlim(-10, 10); ax_map.set_ylim(-10, 10)
            ax_map.set_aspect('equal')
            ax_map.axis('off')
            
            # Dessin des routes
            ax_map.fill_between([-2, 2], -10, 10, color='gray', alpha=0.2)
            ax_map.fill_betweenx([-2, 2], -10, 10, color='gray', alpha=0.2)
            
            # Feux et Files
            colors = {'NS': 'green' if env.phase == 0 else 'red',
                      'EO': 'green' if env.phase == 1 else 'red'}
            if env.orange_restant > 0:
                colors['NS'] = colors['EO'] = 'orange'

            # Position des feux et jauges
            # Nord
            ax_map.add_patch(plt.Circle((0, 3), 0.8, color=colors['NS']))
            ax_map.text(0, 5, f"N: {env.files['N']}", ha='center', fontweight='bold')
            # Sud
            ax_map.add_patch(plt.Circle((0, -3), 0.8, color=colors['NS']))
            ax_map.text(0, -5, f"S: {env.files['S']}", ha='center', fontweight='bold')
            # Est
            ax_map.add_patch(plt.Circle((3, 0), 0.8, color=colors['EO']))
            ax_map.text(5, 0, f"E: {env.files['E']}", va='center', fontweight='bold')
            # Ouest
            ax_map.add_patch(plt.Circle((-3, 0), 0.8, color=colors['EO']))
            ax_map.text(-5, 0, f"O: {env.files['O']}", va='center', fontweight='bold')
            
            ax_map.set_title("VUE DU CARREFOUR", fontsize=12, fontweight='bold')

            # --- 2. HISTORIQUE ---
            ax_main.clear()
            ax_main.plot(history["N"], label="N", alpha=0.8); ax_main.plot(history["E"], label="E", alpha=0.8)
            ax_main.set_title("HISTORIQUE DU TRAFIC")
            ax_main.legend(loc='upper left'); ax_main.grid(True, alpha=0.2)
            
            # --- 3. BARRES DE STATUT ---
            ax_bars.clear()
            dirs = config.DIRECTIONS
            vals = [env.files[d] for d in dirs]
            bar_colors = ['green' if (d in ['N','S'] and env.phase==0) or (d in ['E','O'] and env.phase==1) else 'red' for d in dirs]
            if env.orange_restant > 0: bar_colors = ['orange']*4
            
            ax_bars.bar(dirs, vals, color=bar_colors, edgecolor='black')
            ax_bars.set_title(f"TEMPS RÉEL (Pas {t}) - {'ORANGE' if env.orange_restant>0 else ('VERT NS' if env.phase==0 else 'VERT EO')}")
            ax_bars.set_ylim(0, max(max(vals)+5, 15))

            plt.tight_layout()
            plt.pause(0.05)
            
    except Exception as e:
        print(f"Simulation terminée : {e}")
    finally:
        plt.show()

if __name__ == "__main__":
    # Test heatmap si fichier existe
    path = os.path.join(config.MODELS_DIR, "q_table_equilibre.npy")
    if os.path.exists(path):
        q = np.load(path, allow_pickle=True).item()
        plot_etats_visites(q, os.path.join(config.RESULTS_DIR, "heatmap_etats.png"))
