# SoccerStats Dashboard Guide

## 1. Présentation
Ce guide explique comment lancer, utiliser et adapter le dashboard `dashboard.py`. L'application est construite avec Streamlit et exploite le fichier `top5-players24-25.csv`, qui rassemble 2 852 joueurs issus des cinq principaux championnats européens. Les visualisations sont organisées en quatre onglets complémentaires pour couvrir la répartition des joueurs, l'analyse individuelle, la comparaison entre ligues et les études détaillées.

## 2. Pré-requis
- Python 3.9 ou version supérieure
- Virtualenv (recommandé)
- Dépendances installées via `pip install -r requirements.txt`
- Fichier de données `top5-players24-25.csv` disponible à la racine du projet

## 3. Lancement rapide
```bash
# 1. Activer l'environnement virtuel
source venv/bin/activate

# 2. Installer les dépendances (première utilisation)
pip install -r requirements.txt

# 3. Démarrer le dashboard
streamlit run dashboard.py
```
Le tableau de bord est accessible sur http://localhost:8501 (ou sur le port indiqué par Streamlit).

Pour arrêter le serveur, revenir dans le terminal et utiliser `Ctrl + C`.

## 4. Structure des filtres
La barre latérale propose cinq filtres qui conditionnent toutes les vues :
- **Ligues** : activer une ou plusieurs compétitions
- **Positions** : sélectionner les postes suivis (GB, DF, MI, AT, combinaisons hybrides)
- **Âge** : définir une plage d'âge minimale et maximale
- **Matchs joués** : fixer la tranche d'expérience (MP)
- **Buts minimum** : exclure les joueurs en dessous d'un quota de buts

Chaque modification recharge automatiquement les graphiques et les tableaux. Le compteur de joueurs filtrés s'actualise en haut de page pour indiquer la taille de l'échantillon.

## 5. Navigation par onglets
### 5.1 Vue d'ensemble
- Barres horizontales : distribution des joueurs par position
- Diagramme en anneau : répartition des effectifs par ligue
- Histogramme des dix nations les plus représentées
- Tableaux des dix meilleurs buteurs et passeurs
- Indicateurs moyens (buts par 90, passes par 90, minutes par match)

### 5.2 Analyse individuelle
- Barres comparant les buts par 90 minutes et les passes par 90 minutes par position
- Nuage de points minutes jouées vs buts par 90 minutes (taille = passes par 90)
- Nuage de points buts par 90 vs passes par 90 (taille = minutes par match)
- Nuage de points par niveau d'expérience (plages de matchs joués)
- Classement des quinze meilleures contributions offensives (buts + passes / 90)

### 5.3 Comparaison des ligues
- Tableau récapitulatif des cumuls de buts et de passes par ligue
- Barres groupées illustrant ces volumes
- Tableau et barres groupées des moyennes par joueur (buts par 90, passes par 90)
- Graphique empilé des effectifs par position pour chaque ligue

### 5.4 Analyse détaillée
- Recherche textuelle d'un joueur avec fiche synthétique (indicateurs et radar offensif)
- Comparateur multi-joueurs (jusqu'à quatre profils) avec tableau et radar partagé
- Matrice de corrélation des indicateurs clés (buts/90, passes/90, minutes, MP, âge)
- Nuage de points 3D combinant buts/90, passes/90 et minutes par match
- Tableau filtrable et exportable en CSV (colonnes principales et ratios par 90)

## 6. Indicateurs calculés
| Indicateur | Description |
|------------|-------------|
| `Buts_par_Match` | Buts / matchs joués |
| `Passes_Déc_par_Match` | Passes décisives / matchs joués |
| `Minutes_par_Match` | Minutes / matchs joués |
| `Buts_par_90` | Buts ramenés à 90 minutes |
| `Passes_par_90` | Passes décisives ramenées à 90 minutes |
| `Buts_plus_Passes_90` | Somme buts + passes par 90 minutes |
| `xG_par_90`, `xAG_par_90` | Attendus offensifs par 90 minutes |
| `Matchs_90` | Equivalent matchs complets (colonne `90s`) |

Ces colonnes sont disponibles dans les tableaux et les visualisations quand elles existent dans le CSV source.

## 7. Utilisation du comparateur de joueurs
1. Dans l'onglet "Analyse détaillée", utiliser la recherche pour inspecter un joueur spécifique.
2. Activer le sélecteur multiple "Sélectionner des joueurs à comparer".
3. Choisir jusqu'à quatre joueurs ; les statistiques clés apparaissent dans un tableau dédié.
4. Le radar comparatif met en évidence les différences de production offensive (buts, passes, contributions, xG, xAG par 90 minutes).

## 8. Export et exploitation des données
- Chaque graphique Streamlit dispose d'une icône caméra pour télécharger l'image.
- L'onglet "Analyse détaillée" contient un tableau interactif avec champ de recherche (nom, équipe, ligue) et bouton de téléchargement CSV.
- Les résultats exportés reflètent les filtres actifs au moment du clic.

## 9. Personnalisation rapide
- Les palettes de couleurs ou hauteurs peuvent être adaptées directement dans `dashboard.py` en modifiant les paramètres `color_discrete_map`, `color_discrete_sequence` ou `height` lors de la création des figures Plotly.
- Les plages des niveaux d'expérience sont définies ligne 367 (`pd.cut`). Ajuster les bornes si nécessaire.
- Ajouter de nouvelles colonnes calculées dans la fonction `load_data()` avant le retour du DataFrame.

## 10. Dépannage
| Problème | Vérifications / solutions |
|----------|--------------------------|
| Le serveur ne démarre pas | Vérifier l'activation du virtualenv et l'installation des dépendances (`pip install -r requirements.txt`) |
| Port occupé | Lancer `streamlit run dashboard.py --server.port 8502` |
| Fichier CSV introuvable | Confirmer la présence de `top5-players24-25.csv` à la racine du projet |
| Filtres vides | S'assurer que les colonnes attendues existent dans le CSV et qu'elles ne sont pas vides après filtrage |

## 11. Ressources complémentaires
- Documentation Streamlit : https://docs.streamlit.io
- Documentation Plotly : https://plotly.com/python/
- Guide Pandas : https://pandas.pydata.org/docs/

---
Dernière mise à jour : ajustements du comparateur de joueurs et des visuels inter-ligues.
