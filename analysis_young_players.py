import pandas as pd
import seaborn as sns
import warnings
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

warnings.filterwarnings('ignore')

plt.style.use("seaborn-v0_8")
sns.set(font_scale=1.1)

print("=" * 80)
print("🔵 ANALYSE DES JEUNES JOUEURS - TOP 5 LIGUES EUROPÉENNES")
print("=" * 80)

print("\n📂 Chargement des données...")
PATH = 'top5-players24-25.csv'
df = pd.read_csv(PATH)

print(f"✅ Données chargées : {len(df)} lignes, {len(df.columns)} colonnes")
print("\n📋 Aperçu des données :")
print(df.head())

print("\n" + "=" * 80)
print("🧹 NETTOYAGE DES DONNÉES")
print("=" * 80)

print("\n--- Valeurs Manquantes Totales ---")
total_missing = df.isnull().sum().sum()
if total_missing > 0:
    print(f"Total de valeurs manquantes : {total_missing}")
else:
    print("Aucune valeur manquante dans le dataset.")

print("\n--- Valeurs Manquantes par Colonne ---")
missing_per_column = df.isnull().sum()
missing_per_column = missing_per_column[missing_per_column > 0]
if not missing_per_column.empty:
    print(missing_per_column)
else:
    print("Aucune valeur manquante par colonne.")

print("\n--- Valeurs Dupliquées ---")
total_duplicate = df.duplicated().sum()
if total_duplicate > 0:
    print(f"Total de valeurs dupliquées : {total_duplicate}")
else:
    print("Aucune valeur dupliquée dans le dataset.")

print("\n--- Lignes avec Valeurs Manquantes ---")
missing_rows = df[df['Nation'].isnull() | df['Age'].isnull() | df['Born'].isnull()][['Player', 'Squad', 'Nation', 'Age', 'Born']]
print(missing_rows)

df_cleaned = df.dropna()
print(f"\n✅ Données nettoyées : {len(df_cleaned)} lignes restantes")

print("\n--- Vérification Post-Nettoyage ---")
missing_after = df_cleaned.isnull().sum()
missing_after = missing_after[missing_after > 0]
if missing_after.empty:
    print("✅ Aucune valeur manquante après nettoyage.")
else:
    print(missing_after)

print("\n" + "=" * 80)
print("📊 INFORMATIONS SUR LE DATASET")
print("=" * 80)

print("\n--- Informations Générales ---")
df_cleaned.info()

print("\n--- Statistiques Descriptives ---")
print(df_cleaned.describe())

print("\n" + "=" * 80)
print("📈 ANALYSE DE LA DISTRIBUTION D'ÂGE")
print("=" * 80)

mean_age = df_cleaned['Age'].mean()
median_age = df_cleaned['Age'].median()

print(f"\n📊 Âge moyen des joueurs : {mean_age:.2f} ans")
print(f"📊 Âge médian des joueurs : {median_age:.2f} ans")

fig = px.histogram(
    df_cleaned,
    x="Age",
    nbins=20,
    marginal="box",
    opacity=0.75,
    color_discrete_sequence=['dodgerblue'],
    title="Distribution de l'Âge des Joueurs (Toutes Ligues Confondues)",
)

fig.add_hline(
    y=mean_age,
    line_dash="dash",
    line_color="green",
    annotation_text=f"Moyenne: {mean_age:.2f}",
    annotation_position="top left"
)

fig.add_hline(
    y=median_age,
    line_dash="dot",
    line_color="red",
    annotation_text=f"Médiane: {median_age:.2f}",
    annotation_position="top right"
)

fig.update_layout(title_x=0.5)
fig.show()

leagues = df_cleaned['Comp'].value_counts().head(5).index.tolist()

fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=leagues,
    horizontal_spacing=0.1,
    vertical_spacing=0.15
)

for idx, liga in enumerate(leagues):
    row = idx // 3 + 1
    col = idx % 3 + 1

    data = df_cleaned[df_cleaned['Comp'] == liga]
    mean_age_liga = data['Age'].mean()
    median_age_liga = data['Age'].median()

    fig.add_trace(go.Histogram(
        x=data['Age'],
        nbinsx=20,
        marker_color='dodgerblue',
        opacity=0.75,
        name=liga,
        showlegend=False
    ), row=row, col=col)

    fig.add_vline(
        x=mean_age_liga, line_dash='dash', line_color='green',
        row=row, col=col,
        annotation_text=f"Moy: {mean_age_liga:.1f}",
        annotation_position="top left",
        annotation_font_size=10
    )

    fig.add_vline(
        x=median_age_liga, line_dash='dot', line_color='red',
        row=row, col=col,
        annotation_text=f"Méd: {median_age_liga:.1f}",
        annotation_position="top right",
        annotation_font_size=10
    )

fig.update_layout(
    height=650,
    width=1000,
    title="Distribution de l'Âge des Joueurs par Ligue (Moyenne & Médiane)",
    title_x=0.5,
    bargap=0.05
)

fig.update_xaxes(title_text="Âge")
fig.update_yaxes(title_text="Nombre de Joueurs")

fig.show()

print("\n" + "=" * 80)
print("🏃‍♂️ ANALYSE DES JEUNES JOUEURS")
print("=" * 80)

age_threshold = 21
young_players = df_cleaned[df_cleaned['Age'] <= age_threshold].copy()

print(f"\n🎯 Seuil d'âge : ≤ {age_threshold} ans")
print(f"👥 Nombre de jeunes joueurs : {len(young_players)}")
print(f"📊 Pourcentage du dataset : {len(young_players)/len(df_cleaned)*100:.2f}%")

young_players_per_liga = young_players['Comp'].value_counts().head(5)
print(f"\n📋 Jeunes joueurs par ligue :")
print(young_players_per_liga)

young_players_per_comp = young_players['Comp'].value_counts().head(5).reset_index()
young_players_per_comp.columns = ['Comp', 'Number of Young Players']

fig = px.bar(
    young_players_per_comp,
    x='Number of Young Players',
    y='Comp',
    orientation='h',
    color='Number of Young Players',
    color_continuous_scale='YlGnBu',
    title=f'Nombre de Jeunes Joueurs par Ligue (< {age_threshold} ans)'
)

fig.update_layout(
    xaxis_title="Nombre de Jeunes Joueurs",
    yaxis_title="Ligue",
    yaxis=dict(autorange='reversed'),
    title_x=0.5
)

fig.show()

young_players_per_club = young_players['Squad'].value_counts().head(10).reset_index()
young_players_per_club.columns = ['Squad', 'Number of Young Players']

fig = px.bar(
    young_players_per_club,
    x='Number of Young Players',
    y='Squad',
    orientation='h',
    color='Number of Young Players',
    color_continuous_scale='viridis',
    title=f'Top 10 Clubs avec le Plus de Jeunes Joueurs (< {age_threshold} ans)'
)

fig.update_layout(
    xaxis_title="Nombre de Jeunes Joueurs",
    yaxis_title="Club",
    yaxis=dict(autorange='reversed'),
    title_x=0.5
)

fig.show()

total_per_club = df_cleaned['Squad'].value_counts().reset_index()
total_per_club.columns = ['Squad', 'Total Players']

young_per_club = young_players['Squad'].value_counts().reset_index()
young_per_club.columns = ['Squad', 'Young Players']

proportion_df = pd.merge(total_per_club, young_per_club, on='Squad', how='left')
proportion_df['Young Players'] = proportion_df['Young Players'].fillna(0)
proportion_df['Young Proportion (%)'] = 100 * proportion_df['Young Players'] / proportion_df['Total Players']

top_proportion = proportion_df.sort_values('Young Proportion (%)', ascending=False).head(10)

fig = px.bar(
    top_proportion,
    x='Young Proportion (%)',
    y='Squad',
    orientation='h',
    color='Young Proportion (%)',
    color_continuous_scale='sunsetdark',
    title='Top 10 Clubs avec la Plus Haute Proportion de Jeunes Joueurs'
)

fig.update_layout(
    xaxis_title="Proportion de Jeunes Joueurs (%)",
    yaxis_title="Club",
    yaxis=dict(autorange='reversed'),
    title_x=0.5
)

fig.show()

print("\n" + "=" * 80)
print("⏱️ ANALYSE DES MINUTES ET TITULARISATIONS")
print("=" * 80)

avg_minutes_young = young_players['Min'].mean()
print(f"\n⏱️ Minutes moyennes pour les jeunes joueurs : {avg_minutes_young:.2f} minutes")

avg_min_per_league = young_players.groupby('Comp')['Min'].mean().round(2).sort_values(ascending=False)
print(f"\n📊 Minutes moyennes par ligue :")
print(avg_min_per_league)

fig = px.bar(
    avg_min_per_league.reset_index(),
    x='Min',
    y='Comp',
    orientation='h',
    text='Min',
    color='Min',
    color_continuous_scale='Emrld',
    title='Minutes Moyennes Jouées par les Jeunes Joueurs par Ligue'
)

fig.update_layout(
    yaxis=dict(title='Ligue'),
    xaxis=dict(title='Minutes Moyennes'),
    yaxis_autorange='reversed',
    title_x=0.5
)

fig.show()

top_10_min_young = young_players[['Player', 'Min', 'Age', 'Squad', 'Comp']].sort_values('Min', ascending=False).head(10).reset_index(drop=True)

print(f"\n🏆 Top 10 Jeunes Joueurs avec le Plus de Minutes :")
print(top_10_min_young)

fig = px.bar(
    top_10_min_young,
    x='Min',
    y='Player',
    orientation='h',
    color='Min',
    color_continuous_scale='bupu',
    text='Min',
    title='Top 10 Jeunes Joueurs avec le Plus de Minutes Jouées'
)
fig.update_layout(yaxis=dict(autorange='reversed'), title_x=0.5)
fig.show()

young_players['starter_ratio'] = young_players['Starts'] / young_players['MP']
young_players_filtered = young_players[young_players['MP'] >= 20]
top_starter = young_players_filtered.sort_values(['starter_ratio', 'MP'], ascending=False).head(10)

fig = px.bar(
    top_starter,
    x='Player',
    y='starter_ratio',
    color='starter_ratio',
    color_continuous_scale='viridis',
    title='Ratio de Titularisation des Jeunes Joueurs (Minimum 20 Apparitions)',
    labels={'starter_ratio': 'Ratio de Titularisation'},
    hover_data=['Squad', 'MP', 'Starts', '90s']
)
fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
fig.update_layout(title_x=0.5)
fig.show()

print("\n" + "=" * 80)
print("⚽ ANALYSE DE LA PERFORMANCE OFFENSIVE")
print("=" * 80)

total_goals = df_cleaned['Gls'].sum()
total_assists = df_cleaned['Ast'].sum()
total_ga = df_cleaned['Gls'].add(df_cleaned['Ast']).sum()

young_goals = young_players['Gls'].sum()
young_assists = young_players['Ast'].sum()
young_ga = young_players['Gls'].add(young_players['Ast']).sum()

percent_goals = 100 * young_goals / total_goals
percent_assists = 100 * young_assists / total_assists
percent_ga = 100 * young_ga / total_ga

print(f"\n🎯 Contribution des jeunes joueurs (≤ {age_threshold} ans) :")
print(f"   - Buts : {young_goals} sur {total_goals} ({percent_goals:.2f}%)")
print(f"   - Passes : {young_assists} sur {total_assists} ({percent_assists:.2f}%)")
print(f"   - Total G+A : {young_ga} sur {total_ga} ({percent_ga:.2f}%)")

top_scorers = young_players.sort_values('Gls', ascending=False).head(10)
print(f"\n🥇 Top 10 Jeunes Buteurs :")
print(top_scorers[['Player', 'Squad', 'Age', 'Gls', 'G-PK', 'PK', 'Min']])

top_assisters = young_players.sort_values('Ast', ascending=False).head(10)
print(f"\n🎯 Top 10 Jeunes Passeurs :")
print(top_assisters[['Player', 'Squad', 'Age', 'Ast', 'xAG', 'Min']])

young_players['G+A'] = young_players['Gls'] + young_players['Ast']
top_ga = young_players.sort_values('G+A', ascending=False).head(30)

fig = px.bar(
    top_ga,
    x='G+A',
    y='Player',
    orientation='h',
    text='G+A',
    color='G+A',
    color_continuous_scale='viridis',
    hover_data={
        'Player': True,
        'Gls': True,
        'Ast': True,
        'G+A': True,
        'Age': True,
        'Squad': True,
        'Comp': True
    },
    title=f'Classement des Jeunes Joueurs (≤ {age_threshold} ans) par G+A'
)

fig.update_layout(
    yaxis=dict(autorange='reversed'),
    xaxis_title="Buts + Passes",
    yaxis_title="Joueur",
    title_x=0.5,
    height=800
)

fig.show()

print("\n" + "=" * 80)
print("🧿 ANALYSE DE L'EFFICACITÉ")
print("=" * 80)

young_scorers = df_cleaned[(df_cleaned['Age'] <= age_threshold) & (df_cleaned['Gls'] >= 10)].copy()
young_scorers['conv_Gls_xG'] = young_scorers['Gls'] / young_scorers['xG']
top_efficient_scorers = young_scorers.sort_values('conv_Gls_xG', ascending=False).head(10)

print(f"\n🎯 Top 10 Buteurs les Plus Efficaces (Ratio Buts/xG) :")
print(top_efficient_scorers[['Player', 'Squad', 'Gls', 'xG', 'conv_Gls_xG']])

young_assisters = df_cleaned[(df_cleaned['Age'] <= age_threshold) & (df_cleaned['Ast'] >= df_cleaned['Ast'].quantile(0.95))].copy()
young_assisters['conv_Ast_xAG'] = young_assisters['Ast'] / young_assisters['xAG']
top_efficient_assisters = young_assisters.sort_values('conv_Ast_xAG', ascending=False).head(10)

print(f"\n🎯 Top 10 Passeurs les Plus Efficaces (Ratio Passes/xAG) :")
print(top_efficient_assisters[['Player', 'Squad', 'Ast', 'xAG', 'conv_Ast_xAG']])

print("\n" + "=" * 80)
print("♟ ANALYSE DES POSITIONS")
print("=" * 80)

young_pos_counts = young_players['Pos'].value_counts().reset_index()
young_pos_counts.columns = ['Position', 'Number of Players']

print(f"\n📊 Distribution des Jeunes Joueurs par Position :")
print(young_pos_counts)

fig = px.bar(
    young_pos_counts,
    x='Number of Players',
    y='Position',
    orientation='h',
    text='Number of Players',
    color='Number of Players',
    color_continuous_scale='matter',
    title='Nombre de Jeunes Joueurs par Position'
)

fig.update_layout(
    yaxis=dict(categoryorder='total ascending'),
    title_x=0.5
)

fig.show()

avg_min_per_pos = young_players.groupby('Pos')['Min'].mean().round(2).sort_values(ascending=False).reset_index()
avg_min_per_pos.columns = ['Position', 'Average Minutes']
print(f"\n⏱️ Minutes Moyennes par Position :")
print(avg_min_per_pos)

print("\n" + "=" * 80)
print("🕹 ANALYSE DES PASSES PROGRESSIVES")
print("=" * 80)

top_passes_progressive = young_players[['Player', 'Squad', 'Comp', 'Age', 'PrgP', 'xAG', 'Ast']].sort_values('PrgP', ascending=False).head(10)

print(f"\n🏆 Top 10 Jeunes Joueurs par Passes Progressives :")
print(top_passes_progressive)

fig = px.bar(
    top_passes_progressive.reset_index(),
    x='Player',
    y='PrgP',
    hover_data=['Squad', 'Age', 'Ast', 'PrgP', 'xAG'],
    title='Top 10 Jeunes Joueurs par Passes Progressives (PrgP)',
    color='PrgP',
    color_continuous_scale='tropic'
)
fig.update_layout(title_x=0.5)
fig.show()

young_players['PrgP_xAG'] = young_players['PrgP'] + young_players['xAG']
top_progressors = young_players.sort_values('PrgP_xAG', ascending=False).head(10)
top_progressors_players = top_progressors['Player'].tolist()

fig = px.scatter(
    young_players,
    x='PrgP',
    y='xAG',
    color='Ast',
    size='Ast',
    hover_data=['Player', 'Squad', 'Age'],
    title='Relation entre Passes Progressives et xAG (Taille & Couleur: Passes Décisives)',
    color_continuous_scale='Viridis'
)

for index, row in young_players.iterrows():
    if row['Player'] in top_progressors_players:
        fig.add_annotation(
            x=row['PrgP'],
            y=row['xAG'],
            text=row['Player'],
            showarrow=False,
            yshift=10,
            xshift=0,
            font=dict(size=8, color="black")
        )

fig.update_layout(title_x=0.5)
fig.show()

print("\n" + "=" * 80)
print("🎯 CLUSTERING DES RÔLES DE JOUEURS")
print("=" * 80)

features = ['Gls', 'G-PK', 'xG', 'Ast', 'xAG', 'PrgP', 'CrdY', 'Min']

X = young_players[features].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42)
young_players['RoleCluster'] = kmeans.fit_predict(X_scaled)

pca = PCA(n_components=2)
pca_result = pca.fit_transform(X_scaled)
young_players['PC1'] = pca_result[:, 0]
young_players['PC2'] = pca_result[:, 1]

cluster_summary = young_players.groupby('RoleCluster')[features].mean().round(2)
print("\n📊 Statistiques Moyennes par Cluster :")
print(cluster_summary)

role_map = {
    0: "Finisher",
    1: "Defender",
    2: "Playmaker"
}

young_players['Role'] = young_players['RoleCluster'].map(role_map)

print(f"\n👥 Distribution des Rôles :")
print(young_players['Role'].value_counts())

fig = px.scatter(
    young_players,
    x='PC1',
    y='PC2',
    color='Role',
    hover_data=['Player', 'Squad', 'Age', 'Gls', 'Ast'],
    title='Classification des Rôles des Jeunes Joueurs (Basée sur les Statistiques de Performance)'
)
fig.show()

avg_stats = young_players.groupby('Role')[['Gls', 'Ast', 'xG', 'xAG']].mean().round(2).reset_index()

fig = px.bar(
    avg_stats.melt(id_vars='Role'),
    x='Role',
    y='value',
    color='variable',
    barmode='group',
    title='Statistiques Clés Moyennes par Rôle',
    labels={'value': 'Moyenne', 'variable': 'Statistique'},
    color_discrete_sequence=px.colors.sequential.Viridis
)
fig.update_layout(title_x=0.5)
fig.show()

print("\n" + "=" * 80)
print("💾 EXPORT DES RÉSULTATS")
print("=" * 80)

young_players_export = young_players[['Player', 'Age', 'Squad', 'Comp', 'Pos', 'Role', 'Min', 'Gls', 'Ast', 'G+A', 'xG', 'xAG', 'PrgP', 'starter_ratio']].copy()
young_players_export.to_csv('young_players_analysis.csv', index=False)
print(f"✅ Fichier exporté : young_players_analysis.csv ({len(young_players_export)} lignes)")

top_ga.to_csv('top_30_young_players_ga.csv', index=False)
print(f"✅ Fichier exporté : top_30_young_players_ga.csv (30 lignes)")

cluster_summary.to_csv('role_statistics.csv')
print(f"✅ Fichier exporté : role_statistics.csv (3 rôles)")

print("\n" + "=" * 80)
print("✨ ANALYSE TERMINÉE !")
print("=" * 80)
print(f"\n📁 Fichiers créés :")
print(f"   1. young_players_analysis.csv - Tous les jeunes joueurs avec leurs rôles")
print(f"   2. top_30_young_players_ga.csv - Top 30 par Buts+Passes")
print(f"   3. role_statistics.csv - Statistiques par rôle")
