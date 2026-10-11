# Projet : Gestion Intelligente du Trafic Urbain (Partie 1)
**Cours : IAD & Systèmes Multi-Agents (2025-2026)**

Ce projet implémente un agent intelligent basé sur l'apprentissage par renforcement (**Q-Learning Tabulé**) pour optimiser les cycles d'un feu de signalisation à un carrefour à 4 branches.

---

## 1. Modélisation du MDP
- **États (S)** : Vecteur discret `(qN, qS, qE, qO, phase)`. 
  - Les files d'attente sont discrétisées en 5 niveaux [0, 1, 4, 8, 13] pour limiter l'explosion combinatoire tout en gardant une précision sur la saturation.
  - Phase : 0 (Nord/Sud vert) ou 1 (Est/Ouest vert).
- **Actions (A)** : {0: Maintenir la phase, 1: Changer de phase}.
- **Récompense (R)** : $R = -\sum (\text{véhicules en attente})$. L'objectif est de minimiser le temps d'attente total, ce qui revient mathématiquement à minimiser la longueur cumulée des files.
- **Facteur d'actualisation ($\gamma$)** : 0.95. Choisi pour donner de l'importance aux conséquences à moyen terme (évitement de la saturation future).
- **Dynamique** : Stochastique (arrivées de Poisson), non déterministe, justifiant l'usage du Q-Learning sans connaissance a priori de la matrice de transition $T$.

## 2. Analyse de l'environnement
- **Observabilité** : Partielle (on observe les longueurs de files mais pas les arrivées futures).
- **Déterminisme** : Stochastique (les arrivées suivent une loi de Poisson).
- **Épisodique** : Non-épisodique (flux continu de trafic).
- **Statique/Dynamique** : Dynamique (l'environnement change pendant que l'agent délibère).
- **Discret/Continu** : Discret (pas de temps et actions discrètes).

## 3. Architecture de l'agent
Nous avons choisi une **architecture Hybride** :
- **Réactive** : Pour la gestion immédiate de la phase orange (sécurité).
- **Apprentissage** : Pour l'optimisation des durées de vert via la Q-Table.
*Justification* : Une approche purement délibérative serait trop lente pour le temps réel, tandis qu'une approche purement réactive (comme la baseline) ne s'adapte pas aux variations de trafic.

---

## 4. Installation et Utilisation

### Prérequis
- Python 3.x
- NumPy, Matplotlib

### Installation
```bash
pip install numpy matplotlib
```

### Exécution
1. **Entraînement et Évaluation** :
   ```bash
   python3 main.py --train --eval --scenario equilibre
   python3 main.py --train --eval --scenario asymetrique
   ```
2. **Visualisation temps réel (Démo)** :
   ```bash
   python3 main.py --anim --scenario asymetrique
   ```
3. **Analyse des données pour le rapport** :
   ```bash
   python3 report_generator.py
   ```

---

## 5. Résultats obtenus
- **Scénario Équilibré** : Amélioration de **~65%** par rapport à une alternance fixe.
- **Scénario Asymétrique** : Amélioration de **~88%**. L'agent apprend à maintenir le vert sur l'axe saturé, prouvant l'efficacité de l'apprentissage par rapport à une politique de référence.

Les graphiques de convergence et de comparaison sont disponibles dans le dossier `/results`.
