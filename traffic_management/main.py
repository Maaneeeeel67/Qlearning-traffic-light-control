# fichier: main.py
import argparse
import sys
import os
import config
from training import entrainement
from evaluation import comparer
from visualisation import animation_temps_reel

def main():
    parser = argparse.ArgumentParser(description="Gestion Intelligente de Trafic par Q-Learning")
    parser.add_argument("--train", action="store_true", help="Lancer l'entraînement de l'agent")
    parser.add_argument("--eval", action="store_true", help="Lancer l'évaluation et la comparaison")
    parser.add_argument("--anim", action="store_true", help="Lancer l'animation en temps réel")
    parser.add_argument("--scenario", type=str, default="equilibre", choices=["equilibre", "asymetrique"], 
                        help="Scénario à utiliser (equilibre ou asymetrique)")
    
    args = parser.parse_args()
    
    # Sélection du scénario
    if args.scenario == "equilibre":
        scenario = config.SCENARIO_EQUILIBRE
    else:
        scenario = config.SCENARIO_ASYMMETRIQUE
        
    if args.train:
        entrainement(scenario, args.scenario)
        
    if args.eval:
        comparer(scenario, args.scenario)
        
    if args.anim:
        model_path = os.path.join(config.MODELS_DIR, f"q_table_{args.scenario}.npy")
        if os.path.exists(model_path):
            animation_temps_reel(scenario, model_path)
        else:
            print(f"Erreur : Le modèle {model_path} n'existe pas. Veuillez d'abord l'entraîner avec --train.")

    if not (args.train or args.eval or args.anim):
        parser.print_help()

if __name__ == "__main__":
    main()
