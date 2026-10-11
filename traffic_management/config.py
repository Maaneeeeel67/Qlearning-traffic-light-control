# fichier: config.py
import os

# Paramètres globaux
PAS_PAR_EPISODE = 500
EPISODES = 500
DUREE_ORANGE = 2

# Paramètres Q-Learning
# ALPHA: Compromis entre rapidité d'apprentissage et stabilité (0.1 retenu pour éviter les oscillations)
ALPHA = 0.1           

# GAMMA: Facteur d'actualisation. 0.95 car on s'intéresse à un horizon de ~20 pas.
# Trop bas (0.1) = trop myope. Trop haut (0.99) = trop d'instabilité.
GAMMA = 0.95          

# EPSILON: Stratégie d'exploration. On commence à 1.0 (exploration totale) 
# et on finit à 0.01 (exploitation pure) avec une décroissance exponentielle.
EPSILON_START = 1.0   
EPSILON_END = 0.01    
EPSILON_DECAY = 0.995 

# Discrétisation des files d'attente
# Niveaux : 0 (0 veh), 1 (1-3 veh), 2 (4-7 veh), 3 (8-12 veh), 4 (13+ veh)
SEUILS_DISCRETISATION = [0, 1, 4, 8, 13]

# Scénarios de trafic (Taux d'arrivée Poisson par direction - AUGMENTÉ)
SCENARIO_EQUILIBRE = {"N": 15, "S": 15, "E": 15, "O": 15}
SCENARIO_ASYMMETRIQUE = {"N": 25, "S": 25, "E": 5, "O": 5}

DIRECTIONS = ["N", "S", "E", "O"]

# Chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Création des dossiers si nécessaire
for d in [RESULTS_DIR, MODELS_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)
