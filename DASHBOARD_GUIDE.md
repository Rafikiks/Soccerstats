# 🎮 Guide du Dashboard SoccerStats

## 🚀 Lancement du Dashboard

```bash
# 1. Activer l'environnement virtuel
source venv/bin/activate

# 2. Lancer le dashboard
streamlit run dashboard.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse : **http://localhost:8501**

## 📊 Fonctionnalités du Dashboard

### 🔧 Barre Latérale (Filtres)

Le dashboard offre des filtres interactifs :

1. **Ligues** : Sélectionner une ou plusieurs ligues

   - Premier League, La Liga, Serie A, Bundesliga, Ligue 1

2. **Positions** : Filtrer par position

   - FW (Attaquants), MF (Milieux), DF (Défenseurs), GK (Gardiens)
   - Positions hybrides : FW,MF / DF,MF / etc.

3. **Âge** : Slider pour définir la tranche d'âge

   - Min : 15 ans
   - Max : 41 ans

4. **Matchs Joués (MP)** : Niveau d'expérience

   - Filtrer par nombre de matchs joués

5. **Buts Minimum** : Filtrer les buteurs
   - De 0 à 31 buts

### 📑 Onglets du Dashboard

#### 1️⃣ Vue d'Ensemble

- **Top 10 Buteurs** et **Top 10 Passeurs**
- **Distribution des positions** (graphique en camembert)
- **Buts et Passes par ligue** (graphique en barres)

#### 2️⃣ Buts par Match

- **Moyenne de Buts/Match par Position**
- **Distribution des Buts/Match** (histogramme)
- **Relation MP vs Buts/Match** (scatter plot)
- **Top 20 Joueurs par Buts/Match** (minimum 5 matchs)

#### 3️⃣ Passes par Match

- **Moyenne de Passes/Match par Position**
- **Distribution des Passes/Match** (histogramme)
- **Relation MP vs Passes/Match** (scatter plot)
- **Top 20 Joueurs par Passes/Match** (minimum 5 matchs)

#### 4️⃣ Temps de Jeu

- **Minutes Moyennes par Match par Position**
- **Taux de Titularisation par Position**
- **Distribution des Minutes Totales**
- **Minutes vs Matchs Joués** (scatter plot)
- **Top 20 Joueurs par Minutes Jouées**

#### 5️⃣ Analyse Détaillée

- **Matrice de Corrélation** entre toutes les métriques
- **Analyse 3D Interactive** : Buts/Match, Passes/Match, Minutes/Match
- **Performance par Niveau d'Expérience** :
  - Débutant (1-10 matchs)
  - Intermédiaire (11-20 matchs)
  - Confirmé (21-30 matchs)
  - Expert (31+ matchs)
- **Tableau Complet des Joueurs** (triable et filtrable)
- **Bouton de Téléchargement** pour exporter les données filtrées en CSV

## 🎯 Métriques Calculées

Le dashboard calcule automatiquement :

1. **Buts par Match** : `Gls / MP`
2. **Passes par Match** : `Ast / MP`
3. **Minutes par Match** : `Min / MP`
4. **Niveau d'Expérience** : Basé sur le nombre de matchs joués
5. **Ratio de Titularisation** : `Starts / MP × 100`

## 💡 Cas d'Usage

### 🔍 Scouting de Jeunes Talents

```
1. Filtrer : Âge ≤ 21 ans
2. Filtrer : MP ≥ 10 (expérience minimale)
3. Aller dans "Buts par Match" → Voir les buteurs efficaces
4. Aller dans "Analyse Détaillée" → Télécharger la liste
```

### ⚽ Recherche de Buteurs Prolifiques

```
1. Filtrer : Buts Minimum ≥ 10
2. Filtrer : Position = FW ou FW,MF
3. Onglet "Buts par Match" → Analyser l'efficacité
4. Comparer avec xG dans le tableau détaillé
```

### 🎯 Analyse des Créateurs de Jeu

```
1. Filtrer : Position = MF
2. Filtrer : MP ≥ 20 (réguliers)
3. Onglet "Passes par Match" → Top passeurs
4. Analyser la corrélation avec le temps de jeu
```

### 🏆 Comparaison entre Ligues

```
1. Sélectionner une ligue spécifique
2. Onglet "Vue d'Ensemble" → Voir les statistiques globales
3. Comparer en changeant de ligue
```

## 🎨 Interactivité

Tous les graphiques sont interactifs :

- **Survolez** : Voir les détails d'un point/barre
- **Zoomez** : Cliquez-glissez pour zoomer
- **Cliquez sur la légende** : Masquer/afficher des catégories
- **Double-clic** : Réinitialiser le zoom
- **Export** : Bouton 📷 en haut à droite de chaque graphique

## ⚙️ Configuration Avancée

Pour modifier les couleurs ou le style, éditez `dashboard.py` :

```python
color_discrete_sequence=px.colors.qualitative.Set2
color_continuous_scale='Reds'
```

## 🛑 Arrêter le Dashboard

Dans le terminal où le dashboard tourne :

- Appuyez sur **Ctrl + C**

## 📝 Notes Importantes

- Le dashboard se met à jour automatiquement quand vous modifiez les filtres
- Les calculs sont mis en cache pour de meilleures performances
- Minimum 5 matchs requis pour certains classements (évite les anomalies statistiques)
- Les données sont rechargées automatiquement si le CSV change

## 🆘 Dépannage

### Le dashboard ne se lance pas

```bash
pip install --upgrade streamlit
streamlit run dashboard.py
```

### Erreur de données manquantes

```bash
# Vérifier que le CSV existe
ls -lh top5-players24-25.csv
```

### Port déjà utilisé

```bash
# Utiliser un autre port
streamlit run dashboard.py --server.port 8502
```

## 📞 Support

En cas de problème, vérifiez :

1. ✅ L'environnement virtuel est activé
2. ✅ Toutes les dépendances sont installées
3. ✅ Le fichier CSV est dans le même dossier
4. ✅ Aucun autre Streamlit ne tourne

---

**Bon Scouting ! ⚽🔥**
