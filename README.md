# ⚽ SoccerStats - Analyse des Jeunes Joueurs

Analyse approfondie des jeunes joueurs (≤ 21 ans) dans les 5 meilleures ligues européennes.

## 📊 À Propos

Ce projet analyse les performances des jeunes joueurs en utilisant des métriques avancées :

- **Buts et Passes** : Contributions offensives
- **xG et xAG** : Expected Goals et Expected Assisted Goals
- **Passes Progressives** : Capacité à faire avancer le jeu
- **Clustering** : Classification automatique des rôles (Finisher, Defender, Playmaker)

## 🚀 Installation

### 1. Créer l'environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Sur macOS/Linux
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 📂 Structure du Projet

```
SoccerStats/
├── top5-players24-25.csv          # Dataset principal
├── analysis_young_players.py      # Script d'analyse principal
├── requirements.txt               # Dépendances Python
├── README.md                      # Ce fichier
└── Résultats générés :
    ├── young_players_analysis.csv      # Tous les jeunes joueurs + rôles
    ├── top_30_young_players_ga.csv     # Top 30 par G+A
    └── role_statistics.csv             # Statistiques par rôle
```

## 🎮 Utilisation

### Exécuter l'analyse complète

```bash
python analysis_young_players.py
```

Le script va :

1. ✅ Charger et nettoyer les données
2. 📊 Générer des visualisations interactives (graphiques Plotly)
3. 🔍 Analyser les jeunes joueurs par ligue, club, position
4. 🎯 Calculer l'efficacité (xG, xAG, ratios)
5. 🤖 Classifier les joueurs par rôle (Machine Learning)
6. 💾 Exporter les résultats en CSV

## 📈 Analyses Incluses

### 1. Distribution d'Âge

- Par ligue avec moyennes et médianes
- Identification des ligues les plus jeunes

### 2. Jeunes Joueurs (≤ 21 ans)

- Nombre par ligue et par club
- Proportion dans chaque équipe
- Minutes jouées et ratio de titularisation

### 3. Performance Offensive

- Top buteurs et passeurs
- Contribution totale (G+A)
- Efficacité par rapport à xG et xAG

### 4. Passes Progressives

- Capacité à faire progresser le ballon
- Relation avec xAG

### 5. Clustering des Rôles

- **Finisher** : Buteurs prolifiques
- **Defender** : Joueurs défensifs
- **Playmaker** : Créateurs de jeu

## 🔧 Personnalisation

Vous pouvez modifier les paramètres dans le script :

```python
# Changer le seuil d'âge
age_threshold = 21  # Essayez 18, 19, 23...

# Changer le nombre minimum de buts pour l'analyse d'efficacité
young_scorers = df_cleaned[(df_cleaned['Age'] <= age_threshold) & (df_cleaned['Gls'] >= 10)]
```

## 📝 Colonnes du Dataset

- `Player` : Nom du joueur
- `Age`, `Born` : Âge et année de naissance
- `Squad` : Équipe
- `Comp` : Ligue (Premier League, La Liga, etc.)
- `Pos` : Position (FW, MF, DF, GK)
- `MP`, `Starts`, `Min`, `90s` : Temps de jeu
- `Gls`, `Ast`, `G+A` : Buts et passes
- `xG`, `xAG` : Métriques attendues
- `PrgP`, `PrgC`, `PrgR` : Actions progressives
- `CrdY`, `CrdR` : Cartons

## 🎯 Résultats Exportés

### 1. `young_players_analysis.csv`

Tous les jeunes joueurs avec leur classification :

- Informations personnelles
- Statistiques de performance
- Rôle assigné par clustering

### 2. `top_30_young_players_ga.csv`

Les 30 meilleurs jeunes joueurs par G+A

### 3. `role_statistics.csv`

Statistiques moyennes par rôle (Finisher, Defender, Playmaker)

## 📚 Technologies Utilisées

- **Pandas** : Manipulation de données
- **Plotly** : Visualisations interactives
- **Scikit-learn** : Machine Learning (K-Means, PCA)
- **Seaborn & Matplotlib** : Visualisations supplémentaires

## 💡 Cas d'Usage

- 🔍 **Scouting** : Identifier les jeunes talents prometteurs
- 📊 **Analyse d'équipe** : Comparer les stratégies de développement
- 🎯 **Recrutement** : Trouver des profils spécifiques (buteurs, créateurs)
- 📈 **Stratégie** : Analyser les ligues les plus propices aux jeunes

## 👨‍💻 Auteur

Basé sur le notebook Kaggle de **dzulfikrialwi**  
Adapté pour SoccerStats par **Rafikiks**

## 📄 Licence

Ce projet est à des fins éducatives et d'analyse de données sportives.
