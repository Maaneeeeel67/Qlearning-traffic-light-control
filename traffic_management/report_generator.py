# fichier: report_generator.py
import numpy as np
import os
import config
from agents.q_learning_agent import QLearningAgent

def analyze_q_table(nom_scenario):
    model_path = os.path.join(config.MODELS_DIR, f"q_table_{nom_scenario}.npy")
    if not os.path.exists(model_path):
        print(f"Modèle {nom_scenario} non trouvé. Lancez l'entraînement d'abord.")
        return

    q_table = np.load(model_path, allow_pickle=True).item()
    
    nb_etats_total = len(q_table)
    nb_etats_visites = sum(1 for v in q_table.values() if any(x != 0 for x in v))
    
    print(f"\n--- ANALYSE DU MODÈLE : {nom_scenario} ---")
    print(f"Nombre d'états uniques dans la Q-Table : {nb_etats_total}")
    print(f"Nombre d'états effectivement appris (valeurs non nulles) : {nb_etats_visites}")
    
    # Exemple d'analyse de politique
    # On cherche un état critique (beaucoup de monde au Nord/Sud, personne à l'Est/Ouest, phase NS)
    etat_test = (4, 4, 0, 0, 0) # N=Max, S=Max, E=Min, O=Min, Phase=NS
    if etat_test in q_table:
        q_vals = q_table[etat_test]
        action = "GARDER" if q_vals[0] > q_vals[1] else "CHANGER"
        print(f"Action apprise pour l'état {etat_test} (Fort trafic NS) : {action} (Q: {q_vals})")

    # On cherche l'état inverse
    etat_test_2 = (0, 0, 4, 4, 0) # N=Min, S=Min, E=Max, O=Max, Phase=NS
    if etat_test_2 in q_table:
        q_vals = q_table[etat_test_2]
        action = "GARDER" if q_vals[0] > q_vals[1] else "CHANGER"
        print(f"Action apprise pour l'état {etat_test_2} (Trafic bas NS, Fort EO) : {action} (Q: {q_vals})")

if __name__ == "__main__":
    analyze_q_table("equilibre")
    analyze_q_table("asymetrique")
