# fichier: simulation/trafic_generator.py
import numpy as np
import matplotlib.pyplot as plt
from config import DIRECTIONS

def generer_trafic_poisson(lambda_val, nb_pas):
    """Génère une séquence d'arrivées pour une direction."""
    return np.random.poisson(lambda_val / 60.0, nb_pas)

def visualiser_arrivees(trafic_dict, titre="Distribution des arrivées"):
    """Affiche un histogramme des arrivées."""
    plt.figure(figsize=(10, 6))
    for direction, data in trafic_dict.items():
        plt.plot(data, label=f"Direction {direction}", alpha=0.7)
    plt.title(titre)
    plt.xlabel("Pas de temps")
    plt.ylabel("Nombre de véhicules arrivés")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

if __name__ == "__main__":
    # Test rapide
    test_trafic = {d: generer_trafic_poisson(5, 100) for d in DIRECTIONS}
    visualiser_arrivees(test_trafic)
