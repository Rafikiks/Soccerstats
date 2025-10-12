import streamlit as st
import pandas as pd
import plotly.express as px
import warnings

# Supprimer tous les warnings
warnings.filterwarnings('ignore')
pd.options.mode.chained_assignment = None

st.set_page_config(
    page_title="SoccerStats Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Dashboard des joueurs des 5 plus grandes ligues mondial ")
st.markdown("---")


@st.cache_data
def load_data():
    df = pd.read_csv('top5-players24-25.csv')
    df_cleaned = df.dropna().copy()

    mp_replaced = df_cleaned['MP'].replace(0, pd.NA)
    df_cleaned['Buts par Match'] = (df_cleaned['Gls'] / mp_replaced).fillna(0)
    df_cleaned['Passes Déc par Match'] = (df_cleaned['Ast'] / mp_replaced).fillna(0)
    df_cleaned['Minutes par Match'] = (df_cleaned['Min'] / mp_replaced).fillna(0)

    column_names = {
        'Player': 'Joueur',
        'Nation': 'Nationalité',
        'Squad': 'Équipe',
        'Comp': 'Ligue',
        'Age': 'Âge',
        '90s': 'Matchs 90',
        'Pos': 'Position',
        'MP': 'Matchs Joués',
        'Starts': 'Titularisations',
        'Min': 'Minutes',
        'Gls': 'Buts',
        'Ast': 'Passes Décisives',
        'G+A': 'Buts plus Passes',
        'xG': 'xG',
        'xAG': 'xAG',
        'PrgC': 'Courses Progressives',
        'PrgP': 'Passes Progressives',
        'PrgR': 'Conduites Progressives',
        'Gls_90': 'Performance Buts',
        'Ast_90': 'Performance Passes',
        'G+A_90': 'Performance Buts plus Passes',
        'G-PK_90': 'Performance Buts sans Pénalty',
        'G+A-PK_90': 'Performance Buts plus Passes sans Pénalty',
        'xG_90': 'Performance xG',
        'xAG_90': 'Performance xAG',
        'xG+xAG_90': 'Performance xG plus xAG',
        'npxG': 'npxG',
        'npxG_90': 'Performance npxG',
        'npxG+xAG': 'npxG plus xAG',
        'npxG+xAG_90': 'Performance npxG plus xAG',
        'Buts par Match': 'Buts par Match',
        'Passes_Dec_par_Match': 'Passes Déc par Match'
    }

    df_cleaned = df_cleaned.rename(columns=column_names)

    def translate_position(pos):
        translations = {
            'GK': 'GB',
            'DF': 'DF',
            'MF': 'MI',
            'FW': 'AT',
            'DF,MF': 'DF,MI',
            'MF,DF': 'MI,DF',
            'MF,FW': 'MI,AT',
            'FW,MF': 'AT,MI',
            'DF,FW': 'DF,AT',
            'FW,DF': 'AT,DF'
        }
        return translations.get(pos, pos)

    df_cleaned['Position'] = df_cleaned['Position'].apply(translate_position)

    def translate_nation(nation):
        if pd.isna(nation):
            return nation
        nation_dict = {
            'es ESP': 'Espagne', 'fr FRA': 'France', 'de GER': 'Allemagne',
            'it ITA': 'Italie', 'eng ENG': 'Angleterre', 'br BRA': 'Brésil',
            'ar ARG': 'Argentine', 'pt POR': 'Portugal', 'nl NED': 'Pays-Bas',
            'dk DEN': 'Danemark', 'be BEL': 'Belgique', "ci CIV": "Côte d'Ivoire",
            'ma MAR': 'Maroc', 'ch SUI': 'Suisse', 'se SWE': 'Suède',
            'hr CRO': 'Croatie', 'at AUT': 'Autriche', 'ng NGA': 'Nigeria',
            'us USA': 'États-Unis', 'sct SCO': 'Écosse', 'wal WAL': 'Pays de Galles',
            'sn SEN': 'Sénégal', 'cm CMR': 'Cameroun', 'gh GHA': 'Ghana',
            'co COL': 'Colombie', 'dz ALG': 'Algérie', 'rs SRB': 'Serbie',
            'jp JPN': 'Japon', 'kr KOR': 'Corée du Sud', 'tn TUN': 'Tunisie',
            'uy URU': 'Uruguay', 'tr TUR': 'Turquie', 'pl POL': 'Pologne',
            'cz CZE': 'République Tchèque', 'mx MEX': 'Mexique', 'eg EGY': 'Égypte',
            'nir NIR': 'Irlande du Nord', 'ie IRL': 'Irlande', 'no NOR': 'Norvège',
            'fi FIN': 'Finlande', 'ro ROU': 'Roumanie', 'gr GRE': 'Grèce',
            'hu HUN': 'Hongrie', 'si SVN': 'Slovénie', 'sk SVK': 'Slovaquie',
            'ua UKR': 'Ukraine', 'gn GUI': 'Guinée', 'ga GAB': 'Gabon',
            'ml MLI': 'Mali', 'ao ANG': 'Angola', 'za RSA': 'Afrique du Sud',
            've VEN': 'Venezuela', 'ec ECU': 'Équateur', 'py PAR': 'Paraguay',
            'xk KVX': 'Kosovo', 'al ALB': 'Albanie', 'ba BIH': 'Bosnie-Herzégovine',
            'mk MKD': 'Macédoine du Nord', 'me MNE': 'Monténégro', 'bg BUL': 'Bulgarie',
            'is ISL': 'Islande', 'lu LUX': 'Luxembourg', 'cy CYP': 'Chypre',
            'mt MLT': 'Malte', 'md MDA': 'Moldavie', 'ge GEO': 'Géorgie',
            'am ARM': 'Arménie', 'az AZE': 'Azerbaïdjan', 'kz KAZ': 'Kazakhstan',
            'au AUS': 'Australie', 'nz NZL': 'Nouvelle-Zélande', 'ca CAN': 'Canada',
            'il ISR': 'Israël', 'iq IRQ': 'Irak', 'ir IRN': 'Iran',
            'sa KSA': 'Arabie Saoudite', 'sy SYR': 'Syrie', 'lb LBN': 'Liban',
            'jo JOR': 'Jordanie', 'ps PSE': 'Palestine', 'ae UAE': 'Émirats Arabes Unis'
        }
        return nation_dict.get(nation, nation)

    df_cleaned['Nationalité'] = df_cleaned['Nationalité'].apply(translate_nation)

    numeric_columns = [
        'Buts par Match', 'Passes Déc par Match', 'Minutes par Match',
        'Performance Buts', 'Performance Passes', 'Performance Buts plus Passes',
        'Performance xG', 'Performance xAG', 'Performance xG plus xAG'
    ]
    existing_numeric = [col for col in numeric_columns if col in df_cleaned.columns]
    df_cleaned[existing_numeric] = df_cleaned[existing_numeric].apply(pd.to_numeric, errors='coerce').fillna(0)

    return df_cleaned


df = load_data()

st.sidebar.header("Filtres")

st.sidebar.info(" Aucun filtre est utilisé par défaut.")

selected_leagues = st.sidebar.multiselect(
    "Ligues",
    options=sorted(df['Ligue'].unique()),
    default=[],
    help="Aucune sélection = toutes les ligues"
)

positions = st.sidebar.multiselect(
    "Positions",
    options=sorted(df['Position'].unique()),
    default=[],
    help="Aucune sélection = toutes les positions"
)

# Filtre âge optionnel avec checkbox
filter_age = st.sidebar.checkbox("Filtrer par âge", value=False)
if filter_age:
    age_range = st.sidebar.slider(
        "Âge des joueurs",
        int(df['Âge'].min()),
        int(df['Âge'].max()),
        (int(df['Âge'].min()), int(df['Âge'].max()))
    )
else:
    age_range = (int(df['Âge'].min()), int(df['Âge'].max()))

# Filtre matchs joués optionnel avec checkbox
filter_matches = st.sidebar.checkbox("Filtrer par nombre de matchs", value=False)
if filter_matches:
    mp_range = st.sidebar.slider(
        "Nombre de matchs joués",
        int(df['Matchs Joués'].min()),
        int(df['Matchs Joués'].max()),
        (int(df['Matchs Joués'].min()), int(df['Matchs Joués'].max()))
    )
else:
    mp_range = (int(df['Matchs Joués'].min()), int(df['Matchs Joués'].max()))

# Filtre buts optionnel avec checkbox
filter_goals = st.sidebar.checkbox("Filtrer par nombre de buts", value=False)
if filter_goals:
    min_goals = st.sidebar.slider(
        "Nombre minimum de buts",
        0,
        int(df['Buts'].max()),
        0
    )
else:
    min_goals = 0

# Logique de filtrage : si aucun filtre n'est sélectionné, on affiche tout
league_filter = df['Ligue'].isin(selected_leagues) if selected_leagues else True
position_filter = df['Position'].isin(positions) if positions else True

df_filtered = df[
    league_filter &
    position_filter &
    (df['Âge'] >= age_range[0]) &
    (df['Âge'] <= age_range[1]) &
    (df['Matchs Joués'] >= mp_range[0]) &
    (df['Matchs Joués'] <= mp_range[1]) &
    (df['Buts'] >= min_goals)
]

st.sidebar.markdown("---")

# Compteur de filtres actifs
active_filters = 0
if selected_leagues:
    active_filters += 1
if positions:
    active_filters += 1
if filter_age:
    active_filters += 1
if filter_matches:
    active_filters += 1
if filter_goals and min_goals > 0:
    active_filters += 1

col_metric1, col_metric2 = st.sidebar.columns(2)
col_metric1.metric("Joueurs affichés", len(df_filtered))
col_metric2.metric("Filtres actifs", active_filters)

if active_filters > 0:
    if st.sidebar.button("🔄 Réinitialiser tous les filtres", width='stretch'):
        st.rerun()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Joueurs filtrés", len(df_filtered))

with col2:
    st.metric("Total buts", int(df_filtered['Buts'].sum()))

with col3:
    st.metric("Total passes décisives", int(df_filtered['Passes Décisives'].sum()))

st.markdown("---")


tab_overview, tab_individual, tab_leagues, tab_details = st.tabs([
    "Vue d'ensemble",
    "Analyses performances",
    "Comparaison des ligues",
    "Analyse joueurs"
])

with tab_overview:
    st.header("Vue d'ensemble des statistiques")

    if df_filtered.empty:
        st.write("Aucun joueur ne correspond aux filtres sélectionnés.")
    else:
        position_counts = df_filtered['Position'].value_counts().reset_index()
        position_counts.columns = ['Position', 'Nombre']
        position_counts = position_counts.sort_values('Nombre', ascending=True)

        league_counts = df_filtered['Ligue'].value_counts().reset_index()
        league_counts.columns = ['Ligue', 'Nombre']

        col_distribution, col_leagues = st.columns([1.6, 1])

        with col_distribution:
            fig_positions = px.bar(
                position_counts,
                x='Nombre',
                y='Position',
                orientation='h',
                title='Joueurs par position',
                text='Nombre',
                color='Nombre',
                color_continuous_scale='Viridis'
            )
            fig_positions.update_traces(texttemplate='%{text}', textposition='outside')
            fig_positions.update_layout(height=450, showlegend=False)
            st.plotly_chart(fig_positions, width='stretch')

        with col_leagues:
            fig_leagues = px.pie(
                league_counts,
                names='Ligue',
                values='Nombre',
                hole=0.4,
                title='Répartition par ligue',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_leagues.update_layout(height=450)
            st.plotly_chart(fig_leagues, width='stretch')

        st.markdown("---")

        st.subheader("Nations les plus représentées")
        top_nations = df_filtered['Nationalité'].value_counts().head(10).reset_index()
        top_nations.columns = ['Nationalité', 'Nombre']

        col_nations, col_overview_metrics = st.columns([2, 1])

        with col_nations:
            fig_nations = px.bar(
                top_nations,
                x='Nationalité',
                y='Nombre',
                text='Nombre',
                color='Nombre',
                color_continuous_scale='Blues',
                title='Top 10 des nations'
            )
            fig_nations.update_traces(texttemplate='%{text}', textposition='outside')
            fig_nations.update_layout(height=450, showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig_nations, width='stretch')

        with col_overview_metrics:
            st.metric("Nombre de nations", df_filtered['Nationalité'].nunique())
            st.metric("Nombre d'équipes", df_filtered['Équipe'].nunique())
            st.metric("Ligues couvertes", df_filtered['Ligue'].nunique())
            st.metric("Positions représentées", df_filtered['Position'].nunique())

        st.markdown("---")
        
        st.subheader("Répartition par âge : jeunes talents")
        
        # Créer catégories d'âge
        df_age_split = df_filtered.copy()
        df_age_split['Catégorie'] = df_age_split['Âge'].apply(lambda x: 'Moins de 21 ans' if x < 21 else '21 ans et plus')
        
        col_age1, col_age2 = st.columns([1, 1.5])
        
        with col_age1:
            age_counts = df_age_split['Catégorie'].value_counts().reset_index()
            age_counts.columns = ['Catégorie', 'Nombre']
            age_counts['Pourcentage'] = (age_counts['Nombre'] / age_counts['Nombre'].sum() * 100).round(1)
            
            fig_age_pie = px.pie(
                age_counts,
                names='Catégorie',
                values='Nombre',
                title='Répartition générale par âge',
                hole=0.4,
                color_discrete_sequence=['#A8DADC', '#457B9D']
            )
            fig_age_pie.update_traces(textinfo='percent+label', textposition='inside')
            fig_age_pie.update_layout(height=400)
            st.plotly_chart(fig_age_pie, width='stretch')
        
        with col_age2:
            # Nombre de joueurs par catégorie d'âge et par ligue
            league_age_detail = df_age_split.groupby(['Ligue', 'Catégorie']).size().reset_index(name='Nombre')
            
            fig_age_league = px.bar(
                league_age_detail,
                x='Ligue',
                y='Nombre',
                color='Catégorie',
                title='Répartition jeunes vs expérimentés par ligue',
                text='Nombre',
                barmode='group',
                color_discrete_sequence=['#A8DADC', '#457B9D']
            )
            fig_age_league.update_traces(texttemplate='%{text}', textposition='outside')
            fig_age_league.update_layout(
                height=400,
                yaxis_title="Nombre de joueurs",
                xaxis_title="Ligue",
                legend_title_text="Catégorie d'âge"
            )
            st.plotly_chart(fig_age_league, width='stretch')

        st.markdown("---")

        st.subheader("Indicateurs globaux")
        col_global_1, col_global_2, col_global_3 = st.columns(3)
        col_global_1.metric("Performance Buts moyenne", f"{df_filtered['Performance Buts'].mean():.2f}")
        col_global_2.metric("Performance Passes moyenne", f"{df_filtered['Performance Passes'].mean():.2f}")
        col_global_3.metric("Minutes moyennes par match", f"{df_filtered['Minutes par Match'].mean():.1f}")

with tab_individual:
    st.header("Analyses performances")

    if df_filtered.empty:
        st.write("Aucun joueur ne correspond aux filtres sélectionnés.")
    else:
        st.subheader("Moyennes offensives par position")
        position_performance = df_filtered.groupby('Position').agg({
            'Performance Buts': 'mean',
            'Performance Passes': 'mean'
        }).reset_index()

        col_perf_1, col_perf_2 = st.columns(2)

        with col_perf_1:
            fig_goals90 = px.bar(
                position_performance.sort_values('Performance Buts', ascending=False),
                x='Position',
                y='Performance Buts',
                color='Performance Buts',
                color_continuous_scale='Reds',
                title='Performance Buts moyenne par position',
                text='Performance Buts'
            )
            fig_goals90.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_goals90.update_layout(height=420, showlegend=False)
            st.plotly_chart(fig_goals90, width='stretch')

        with col_perf_2:
            fig_assists90 = px.bar(
                position_performance.sort_values('Performance Passes', ascending=False),
                x='Position',
                y='Performance Passes',
                color='Performance Passes',
                color_continuous_scale='Blues',
                title='Performance Passes moyenne par position',
                text='Performance Passes'
            )
            fig_assists90.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_assists90.update_layout(height=420, showlegend=False)
            st.plotly_chart(fig_assists90, width='stretch')

        st.markdown("---")

        st.subheader("Temps de jeu et rendement offensif")
        fig_minutes_goals = px.scatter(
            df_filtered,
            x='Minutes',
            y='Performance Buts',
            color='Position',
            size='Performance Passes',
            hover_data=['Joueur', 'Équipe', 'Matchs Joués', 'Buts', 'Passes Décisives', 'Performance Passes'],
            title='Minutes jouées vs Performance Buts',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_minutes_goals.update_layout(height=450)
        st.plotly_chart(fig_minutes_goals, width='stretch')

        col_scatter_1, col_scatter_2 = st.columns(2)

        with col_scatter_1:
            fig_goals_assists = px.scatter(
                df_filtered,
                x='Performance Buts',
                y='Performance Passes',
                size='Minutes par Match',
                color='Position',
                hover_data=['Joueur', 'Équipe', 'Matchs Joués'],
                title='Performance Buts vs Performance Passes',
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig_goals_assists.update_layout(height=420)
            st.plotly_chart(fig_goals_assists, width='stretch')

        with col_scatter_2:
            upper_limit = max(int(df_filtered['Matchs Joués'].max()), 31)
            experience_view = df_filtered.copy()
            experience_view['Niveau Expérience'] = pd.cut(
                experience_view['Matchs Joués'],
                bins=[0, 10, 20, 30, upper_limit + 1],
                labels=['Débutant (1-10)', 'Intermédiaire (11-20)', 'Confirmé (21-30)', 'Expert (31+)'],
                right=False,
                include_lowest=True
            )
            fig_experience = px.scatter(
                experience_view,
                x='Matchs Joués',
                y='Performance Buts',
                color='Niveau Expérience',
                size='Performance Passes',
                hover_data=['Joueur', 'Équipe', 'Position', 'Minutes par Match'],
                title="Rendement offensif selon l'expérience",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_experience.update_layout(height=420)
            st.plotly_chart(fig_experience, width='stretch')

        st.markdown("---")

        st.subheader("Matrice de corrélation")
        
        correlation_columns = ['Performance Buts', 'Performance Passes', 'Minutes par Match', 'Matchs Joués', 'Âge']
        correlation_data = df_filtered[correlation_columns].corr() if not df_filtered.empty else pd.DataFrame(columns=correlation_columns)
        
        if not correlation_data.empty:
            fig_corr = px.imshow(
                correlation_data,
                text_auto='.2f',
                aspect='auto',
                color_continuous_scale='RdBu_r',
                title='Corrélations des indicateurs clés'
            )
            fig_corr.update_layout(height=500)
            st.plotly_chart(fig_corr, width='stretch')
        else:
            st.write("La matrice de corrélation est disponible lorsque des joueurs sont filtrés.")

        st.markdown("---")

        st.subheader("Analyse multi-dimensionnelle")
        
        if not df_filtered.empty:
            fig_scatter_3d = px.scatter_3d(
                df_filtered,
                x='Performance Buts',
                y='Performance Passes',
                z='Minutes par Match',
                color='Position',
                size='Matchs Joués',
                hover_data=['Joueur', 'Équipe', 'Âge'],
                title='Performance Buts, Passes et Minutes par match'
            )
            fig_scatter_3d.update_layout(height=600)
            st.plotly_chart(fig_scatter_3d, width='stretch')
        else:
            st.write("L'analyse multi-dimensionnelle nécessite au moins un joueur filtré.")

        st.markdown("---")

        st.subheader("Évolution de la performance avec l'âge")
        
        # Performance moyenne par âge
        age_performance = df_filtered.groupby('Âge', observed=False).agg({
            'Performance Buts': 'mean',
            'Performance Passes': 'mean',
            'Joueur': 'count'
        }).reset_index()
        age_performance.columns = ['Âge', 'Performance Buts Moyenne', 'Performance Passes Moyenne', 'Nombre Joueurs']
        
        # Filtrer les âges avec au moins 10 joueurs pour éviter les outliers
        age_performance = age_performance[age_performance['Nombre Joueurs'] >= 10]
        
        fig_age = px.line(
            age_performance,
            x='Âge',
            y=['Performance Buts Moyenne', 'Performance Passes Moyenne'],
            title='Évolution de la performance avec l\'âge',
            labels={'value': 'Performance moyenne', 'variable': 'Métrique', 'Âge': 'Âge'},
            markers=True
        )
        fig_age.update_layout(height=450, legend_title_text='Métrique')
        st.plotly_chart(fig_age, width='stretch')

with tab_leagues:
    st.header("Comparaison des ligues")

    if df_filtered.empty:
        st.write("Aucune donnée à comparer pour les filtres actuels.")
    else:
        st.subheader("Volumes cumulés")
        league_totals = df_filtered.groupby('Ligue')[['Buts', 'Passes Décisives']].sum().reset_index()
        league_totals = league_totals.sort_values('Buts', ascending=False)
        st.dataframe(league_totals, hide_index=True, width='stretch')

        league_totals_long = league_totals.melt(id_vars='Ligue', var_name='Statistique', value_name='Valeur')

        fig_league_totals = px.bar(
            league_totals_long,
            x='Ligue',
            y='Valeur',
            color='Statistique',
            barmode='group',
            title='Buts et passes décisives cumulés par ligue',
            color_discrete_map={
                'Buts': '#EF553B',
                'Passes Décisives': '#636EFA'
            }
        )
        fig_league_totals.update_layout(height=480, xaxis_title='Ligue', yaxis_title='Volume cumulé')
        st.plotly_chart(fig_league_totals, width='stretch')

        st.markdown("---")

        st.subheader("Moyennes par joueur")
        league_means = df_filtered.groupby('Ligue')[['Performance Buts', 'Performance Passes']].mean().reset_index()
        league_means = league_means.sort_values('Performance Buts', ascending=False)
        st.dataframe(league_means.round(3), hide_index=True, width='stretch')

        league_means_long = league_means.melt(id_vars='Ligue', var_name='Indicateur', value_name='Valeur')

        fig_league_means = px.bar(
            league_means_long,
            x='Ligue',
            y='Valeur',
            color='Indicateur',
            barmode='group',
            title='Performance moyenne par joueur et par ligue',
            color_discrete_map={
                'Performance Buts': '#EF553B',
                'Performance Passes': '#636EFA'
            }
        )
        fig_league_means.update_layout(height=480, xaxis_title='Ligue', yaxis_title='Valeur moyenne')
        st.plotly_chart(fig_league_means, width='stretch')

        st.markdown("---")

        st.subheader("Répartition des positions")
        positions_league = df_filtered.groupby(['Ligue', 'Position']).size().reset_index(name='Nombre')
        fig_positions_league = px.bar(
            positions_league,
            x='Ligue',
            y='Nombre',
            color='Position',
            barmode='stack',
            title='Composition des effectifs par position et par ligue'
        )
        fig_positions_league.update_layout(height=500, xaxis_title='Ligue', yaxis_title='Nombre de joueurs')
        st.plotly_chart(fig_positions_league, width='stretch')

with tab_details:
    st.header("Analyse joueurs")
    
    if df_filtered.empty:
        st.write("Aucun joueur ne correspond aux filtres sélectionnés.")
    else:
        # SECTION 1 : Recherche et fiche individuelle
        st.subheader("Recherche et fiche joueur")
        
        player_names = sorted(df_filtered['Joueur'].unique())
        
        if not player_names:
            st.write("Aucun joueur ne correspond aux filtres sélectionnés.")
        else:
            player_choice = st.selectbox(
                "Sélectionner un joueur à analyser",
                options=player_names,
                key="player_choice",
                help="Utilisez la barre de recherche pour filtrer les joueurs par nom"
            )
            
            selected_player = df_filtered[df_filtered['Joueur'] == player_choice].iloc[0]

            info_cols = st.columns(4)
            info_cols[0].write(f"**Joueur :** {selected_player['Joueur']}")
            info_cols[1].write(f"**Âge :** {selected_player['Âge']}")
            info_cols[2].write(f"**Équipe :** {selected_player['Équipe']}")
            info_cols[3].write(f"**Ligue :** {selected_player['Ligue']}")

            stat_cols = st.columns(3)
            stat_cols[0].metric("Matchs joués", int(selected_player['Matchs Joués']))
            stat_cols[1].metric("Buts", int(selected_player['Buts']))
            stat_cols[2].metric("Passes décisives", int(selected_player['Passes Décisives']))

            ratio_cols = st.columns(3)
            ratio_cols[0].metric("Buts par match", f"{selected_player['Buts par Match']:.3f}")
            ratio_cols[1].metric("Passes décisives par match", f"{selected_player['Passes Déc par Match']:.3f}")
            ratio_cols[2].metric("Minutes par match", f"{selected_player['Minutes par Match']:.1f}")

            radar_metrics = [
                ('Performance Buts', 'Buts'),
                ('Performance Passes', 'Passes'),
                ('Performance Buts plus Passes', 'Buts+Passes'),
                ('Performance xG', 'xG'),
                ('Performance xAG', 'xAG')
            ]
            radar_data = []
            for metric, label in radar_metrics:
                if metric in selected_player.index:
                    value = pd.to_numeric(pd.Series([selected_player[metric]]), errors='coerce').fillna(0).iloc[0]
                    radar_data.append({'Indicateur': label, 'Valeur': float(value)})

            radar_df = pd.DataFrame(radar_data)
            if not radar_df.empty and radar_df['Valeur'].max() > 0:
                fig_radar = px.line_polar(
                    radar_df,
                    r='Valeur',
                    theta='Indicateur',
                    line_close=True,
                    range_r=[0, radar_df['Valeur'].max() * 1.1]
                )
                fig_radar.update_traces(fill='toself')
                fig_radar.update_layout(height=420, margin=dict(l=40, r=40, t=60, b=40))
                st.plotly_chart(fig_radar, width='stretch')
            else:
                st.write("Données insuffisantes pour générer un radar pour ce joueur.")
        
            
            st.markdown("---")
            
            # SECTION 2 : Comparateur de joueurs
            st.subheader("Comparateur de joueurs")
            
            compare_players = st.multiselect(
                "Sélectionner des joueurs à comparer (maximum 4)",
                options=player_names,
                key="player_compare"
            )

            if compare_players:
                if len(compare_players) > 4:
                    st.warning("Seuls les quatre premiers joueurs sélectionnés seront affichés.")
                    compare_players = compare_players[:4]

                compare_df = df_filtered[df_filtered['Joueur'].isin(compare_players)].copy()

                if compare_df.empty:
                    st.write("Aucun joueur ne correspond à cette sélection pour les filtres actuels.")
                else:
                    compare_columns = [
                        'Joueur', 'Position', 'Équipe', 'Ligue', 'Matchs Joués', 'Minutes',
                        'Buts', 'Passes Décisives', 'Performance Buts', 'Performance Passes',
                        'Performance Buts plus Passes', 'Performance xG', 'Performance xAG'
                    ]
                    available_compare_columns = [col for col in compare_columns if col in compare_df.columns]
                    compare_table = compare_df[available_compare_columns].copy()

                    numeric_compare_cols = [
                        col for col in available_compare_columns
                        if pd.api.types.is_numeric_dtype(compare_table[col])
                    ]
                    compare_table[numeric_compare_cols] = compare_table[numeric_compare_cols].apply(lambda s: s.round(3))

                    st.dataframe(compare_table, hide_index=True, width='stretch')

                    radar_metrics_map = {
                        'Performance Buts': 'Buts',
                        'Performance Passes': 'Passes',
                        'Performance Buts plus Passes': 'Buts+Passes',
                        'Performance xG': 'xG',
                        'Performance xAG': 'xAG'
                    }
                    available_radar_metrics = [
                        metric for metric in radar_metrics_map.keys() if metric in compare_df.columns
                    ]

                    radar_source = compare_df[['Joueur'] + available_radar_metrics].copy()
                    radar_long = radar_source.melt(id_vars='Joueur', var_name='Indicateur', value_name='Valeur')
                    radar_long['Indicateur'] = radar_long['Indicateur'].replace(radar_metrics_map)

                    if not radar_long.empty and radar_long['Valeur'].abs().sum() > 0:
                        fig_compare_radar = px.line_polar(
                            radar_long,
                            r='Valeur',
                            theta='Indicateur',
                            color='Joueur',
                            line_close=True
                        )
                        fig_compare_radar.update_traces(fill='toself')
                        fig_compare_radar.update_layout(height=500, margin=dict(t=60, l=40, r=40, b=40))
                        st.plotly_chart(fig_compare_radar, width='stretch')
                    else:
                        st.write("Les indicateurs sélectionnés ne permettent pas de générer un radar comparatif.")
            else:
                st.write("Sélectionnez un ou plusieurs joueurs pour lancer la comparaison.")
        
        st.markdown("---")
        
        # SECTION 3 : Classements et tops
        st.subheader("Classements et tops")
        
        col_top1, col_top2 = st.columns(2)
        
        with col_top1:
            top_scorers = df_filtered.nlargest(15, 'Buts')[
                ['Joueur', 'Équipe', 'Position', 'Buts', 'Performance Buts']
            ].copy()
            top_scorers['Label'] = top_scorers['Joueur'] + ' (' + top_scorers['Équipe'] + ')'
            
            fig_top_scorers = px.bar(
                top_scorers,
                y='Label',
                x='Buts',
                orientation='h',
                title='Top 15 buteurs',
                text='Buts',
                color='Position',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hover_data=['Joueur', 'Équipe', 'Position', 'Buts', 'Performance Buts']
            )
            fig_top_scorers.update_traces(texttemplate='%{text}', textposition='outside')
            fig_top_scorers.update_layout(
                yaxis=dict(autorange='reversed'),
                height=500,
                yaxis_title="",
                xaxis_title="Nombre de buts"
            )
            st.plotly_chart(fig_top_scorers, width='stretch')
        
        with col_top2:
            top_assisters = df_filtered.nlargest(15, 'Passes Décisives')[
                ['Joueur', 'Équipe', 'Position', 'Passes Décisives', 'Performance Passes']
            ].copy()
            top_assisters['Label'] = top_assisters['Joueur'] + ' (' + top_assisters['Équipe'] + ')'
            
            fig_top_assisters = px.bar(
                top_assisters,
                y='Label',
                x='Passes Décisives',
                orientation='h',
                title='Top 15 passeurs',
                text='Passes Décisives',
                color='Position',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hover_data=['Joueur', 'Équipe', 'Position', 'Passes Décisives', 'Performance Passes']
            )
            fig_top_assisters.update_traces(texttemplate='%{text}', textposition='outside')
            fig_top_assisters.update_layout(
                yaxis=dict(autorange='reversed'),
                height=500,
                yaxis_title="",
                xaxis_title="Nombre de passes décisives"
            )
            st.plotly_chart(fig_top_assisters, width='stretch')
        
        st.caption("Joueurs ayant joué au moins 5 matchs")
        top_contributions = df_filtered[df_filtered['Matchs Joués'] >= 5].nlargest(20, 'Performance Buts plus Passes')
        
        if not top_contributions.empty:
            top_contributions_display = top_contributions.copy()
            top_contributions_display['Label'] = top_contributions_display['Joueur'] + ' (' + top_contributions_display['Équipe'] + ')'
            
            fig_top_contrib = px.bar(
                top_contributions_display,
                y='Label',
                x='Performance Buts plus Passes',
                orientation='h',
                title='Top 20 contributions offensives totales',
                text='Performance Buts plus Passes',
                color='Position',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hover_data=['Joueur', 'Équipe', 'Position', 'Matchs Joués', 'Performance Buts', 'Performance Passes']
            )
            fig_top_contrib.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_top_contrib.update_layout(
                yaxis=dict(autorange='reversed'),
                height=600,
                yaxis_title="",
                xaxis_title="Performance Buts + Passes"
            )
            st.plotly_chart(fig_top_contrib, width='stretch')
        else:
            st.info("Aucun joueur n'a joué au moins 5 matchs dans cette sélection.")
    
    st.markdown("---")
    
    # SECTION 4 : Tableau complet et export
    st.subheader("Tableau complet et export")

    base_columns = [
        'Joueur', 'Âge', 'Équipe', 'Ligue', 'Position', 'Matchs Joués', 'Minutes',
        'Buts', 'Passes Décisives', 'Buts par Match', 'Passes Déc par Match',
        'Minutes par Match', 'Performance Buts', 'Performance Passes', 'Performance Buts plus Passes',
        'Performance xG', 'Performance xAG'
    ]
    available_columns = [col for col in base_columns if col in df_filtered.columns]
    display_df = df_filtered[available_columns].copy()

    if not display_df.empty:
        round_columns = [
            'Buts par Match', 'Passes Déc par Match', 'Minutes par Match',
            'Performance Buts', 'Performance Passes', 'Performance Buts plus Passes', 'Performance xG', 'Performance xAG'
        ]
        for column in round_columns:
            if column in display_df.columns:
                display_df[column] = display_df[column].round(3)
        if 'Minutes par Match' in display_df.columns:
            display_df['Minutes par Match'] = display_df['Minutes par Match'].round(1)

        sort_columns = [col for col in ['Performance Buts plus Passes', 'Buts'] if col in display_df.columns]
        if sort_columns:
            display_df = display_df.sort_values(sort_columns, ascending=[False] + [False] * (len(sort_columns) - 1))

        table_search = st.text_input(
            "Filtrer le tableau (nom, équipe ou ligue)",
            placeholder="Exemple : Madrid",
            key="table_search"
        )

        if table_search:
            mask = (
                display_df['Joueur'].str.contains(table_search, case=False, na=False) |
                display_df['Équipe'].str.contains(table_search, case=False, na=False) |
                display_df['Ligue'].str.contains(table_search, case=False, na=False)
            )
            filtered_table_df = display_df[mask]
        else:
            filtered_table_df = display_df

        st.dataframe(
            filtered_table_df,
            width='stretch',
            hide_index=True,
            height=400
        )

        csv = filtered_table_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les données filtrées (CSV)",
            data=csv,
            file_name='joueurs_filtres.csv',
            mime='text/csv'
        )
    else:
        st.write("Aucun joueur à afficher dans le tableau.")

st.markdown("---")

st.info("""
*Comment utiliser ce dashboard :*

*Visualisation par défaut : Toutes les données sont affichées au départ pour une vue d'ensemble complète.*

*Filtrage progressif :*
- Utilisez les filtres dans la barre latérale pour affiner progressivement votre sélection.
- Pour les ligues et positions : sélectionnez une ou plusieurs options. Aucune sélection = toutes les données.
- Pour l'âge, les matchs et les buts : cochez la case pour activer le filtre, puis ajustez avec le curseur.
- Le compteur "Filtres actifs" vous indique combien de critères sont appliqués.
- Utilisez le bouton "Réinitialiser" pour revenir à la vue complète.

*Navigation :*
- Explorez les 4 onglets pour différentes analyses : vue d'ensemble, performances, ligues et joueurs.
- Survolez les graphiques pour plus d'informations (zoom, détails, légendes interactives).
- Téléchargez les données filtrées en CSV depuis l'onglet "Analyse joueurs".

*Métriques expliquées :*
- *Buts par Match* = nombre de buts ÷ matchs joués
- *Passes Déc par Match* = passes décisives ÷ matchs joués
- *Performance Buts / Performance Passes* = production standardisée par match
- *Performance xG* = Expected Goals (buts attendus statistiquement)
- *Performance xAG* = Expected Assists (passes attendues statistiquement)
- *Minutes par Match* = minutes ÷ matchs joués
""")
