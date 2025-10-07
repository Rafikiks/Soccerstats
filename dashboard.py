import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SoccerStats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Dashboard d'analyse des statistiques des joueurs")
st.markdown("---")


@st.cache_data
def load_data():
    df = pd.read_csv('top5-players24-25.csv')
    df_cleaned = df.dropna().copy()

    mp_replaced = df_cleaned['MP'].replace(0, pd.NA)
    df_cleaned['Buts_par_Match'] = (df_cleaned['Gls'] / mp_replaced).fillna(0)
    df_cleaned['Passes_Dec_par_Match'] = (df_cleaned['Ast'] / mp_replaced).fillna(0)
    df_cleaned['Minutes_par_Match'] = (df_cleaned['Min'] / mp_replaced).fillna(0)

    column_names = {
        'Player': 'Joueur',
        'Nation': 'Nationalité',
        'Squad': 'Équipe',
        'Comp': 'Ligue',
        'Age': 'Âge',
        '90s': 'Matchs_90',
        'Pos': 'Position',
        'MP': 'Matchs_Joués',
        'Starts': 'Titularisations',
        'Min': 'Minutes',
        'Gls': 'Buts',
        'Ast': 'Passes_Décisives',
        'G+A': 'Buts_plus_Passes',
        'xG': 'xG',
        'xAG': 'xAG',
        'PrgC': 'Courses_Progressives',
        'PrgP': 'Passes_Progressives',
        'PrgR': 'Conduites_Progressives',
        'Gls_90': 'Buts_par_90',
        'Ast_90': 'Passes_par_90',
        'G+A_90': 'Buts_plus_Passes_90',
        'G-PK_90': 'Buts_sans_Pénalty_90',
        'G+A-PK_90': 'Buts_plus_Passes_sans_Pénalty_90',
        'xG_90': 'xG_par_90',
        'xAG_90': 'xAG_par_90',
        'xG+xAG_90': 'xG_plus_xAG_90',
        'npxG': 'npxG',
        'npxG_90': 'npxG_par_90',
        'npxG+xAG': 'npxG_plus_xAG',
        'npxG+xAG_90': 'npxG_plus_xAG_90',
        'Buts_par_Match': 'Buts_par_Match',
        'Passes_Dec_par_Match': 'Passes_Déc_par_Match'
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
        'Buts_par_Match', 'Passes_Déc_par_Match', 'Minutes_par_Match',
        'Buts_par_90', 'Passes_par_90', 'Buts_plus_Passes_90',
        'xG_par_90', 'xAG_par_90', 'xG_plus_xAG_90'
    ]
    existing_numeric = [col for col in numeric_columns if col in df_cleaned.columns]
    df_cleaned[existing_numeric] = df_cleaned[existing_numeric].apply(pd.to_numeric, errors='coerce').fillna(0)

    return df_cleaned


df = load_data()

st.sidebar.header("Filtres")

selected_leagues = st.sidebar.multiselect(
    "Sélectionner les ligues",
    options=sorted(df['Ligue'].unique()),
    default=sorted(df['Ligue'].unique())
)

positions = st.sidebar.multiselect(
    "Sélectionner les positions",
    options=sorted(df['Position'].unique()),
    default=sorted(df['Position'].unique())
)

age_range = st.sidebar.slider(
    "Âge des joueurs",
    int(df['Âge'].min()),
    int(df['Âge'].max()),
    (int(df['Âge'].min()), int(df['Âge'].max()))
)

mp_range = st.sidebar.slider(
    "Nombre de matchs joués",
    int(df['Matchs_Joués'].min()),
    int(df['Matchs_Joués'].max()),
    (int(df['Matchs_Joués'].min()), int(df['Matchs_Joués'].max()))
)

min_goals = st.sidebar.slider(
    "Nombre minimum de buts",
    0,
    int(df['Buts'].max()),
    0
)

df_filtered = df[
    (df['Ligue'].isin(selected_leagues)) &
    (df['Position'].isin(positions)) &
    (df['Âge'] >= age_range[0]) &
    (df['Âge'] <= age_range[1]) &
    (df['Matchs_Joués'] >= mp_range[0]) &
    (df['Matchs_Joués'] <= mp_range[1]) &
    (df['Buts'] >= min_goals)
]

st.sidebar.markdown("---")
st.sidebar.metric("Total joueurs filtrés", len(df_filtered))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Joueurs filtrés", len(df_filtered))

with col2:
    st.metric("Total buts", int(df_filtered['Buts'].sum()))

with col3:
    st.metric("Total passes décisives", int(df_filtered['Passes_Décisives'].sum()))

st.markdown("---")


tab_overview, tab_individual, tab_leagues, tab_details = st.tabs([
    "Vue d'ensemble",
    "Analyse individuelle",
    "Comparaison des ligues",
    "Analyse détaillée"
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
            st.plotly_chart(fig_positions, use_container_width=True)

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
            st.plotly_chart(fig_leagues, use_container_width=True)

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
            st.plotly_chart(fig_nations, use_container_width=True)

        with col_overview_metrics:
            st.metric("Nombre de nations", df_filtered['Nationalité'].nunique())
            st.metric("Nombre d'équipes", df_filtered['Équipe'].nunique())
            st.metric("Ligues couvertes", df_filtered['Ligue'].nunique())
            st.metric("Positions représentées", df_filtered['Position'].nunique())

        st.markdown("---")

        st.subheader("Performers offensifs")
        col_top_scorers, col_top_assisters = st.columns(2)

        with col_top_scorers:
            st.write("Top 10 buteurs")
            top_scorers = df_filtered.nlargest(10, 'Buts')[
                ['Joueur', 'Position', 'Équipe', 'Ligue', 'Buts', 'Matchs_Joués', 'Buts_par_90']
            ].copy()
            if not top_scorers.empty:
                top_scorers['Buts_par_90'] = top_scorers['Buts_par_90'].round(2)
            st.dataframe(top_scorers, width='stretch', hide_index=True)

        with col_top_assisters:
            st.write("Top 10 passeurs décisifs")
            top_assisters = df_filtered.nlargest(10, 'Passes_Décisives')[
                ['Joueur', 'Position', 'Équipe', 'Ligue', 'Passes_Décisives', 'Matchs_Joués', 'Passes_par_90']
            ].copy()
            if not top_assisters.empty:
                top_assisters['Passes_par_90'] = top_assisters['Passes_par_90'].round(2)
            st.dataframe(top_assisters, width='stretch', hide_index=True)

        st.markdown("---")

        st.subheader("Indicateurs globaux")
        col_global_1, col_global_2, col_global_3 = st.columns(3)
        col_global_1.metric("Buts moyens par 90 minutes", f"{df_filtered['Buts_par_90'].mean():.2f}")
        col_global_2.metric("Passes décisives moyennes par 90 minutes", f"{df_filtered['Passes_par_90'].mean():.2f}")
        col_global_3.metric("Minutes moyennes par match", f"{df_filtered['Minutes_par_Match'].mean():.1f}")

with tab_individual:
    st.header("Analyse individuelle")

    if df_filtered.empty:
        st.write("Aucun joueur ne correspond aux filtres sélectionnés.")
    else:
        st.subheader("Moyennes offensives par position (par 90 minutes)")
        position_performance = df_filtered.groupby('Position').agg({
            'Buts_par_90': 'mean',
            'Passes_par_90': 'mean'
        }).reset_index()

        col_perf_1, col_perf_2 = st.columns(2)

        with col_perf_1:
            fig_goals90 = px.bar(
                position_performance.sort_values('Buts_par_90', ascending=False),
                x='Position',
                y='Buts_par_90',
                color='Buts_par_90',
                color_continuous_scale='Reds',
                title='Buts moyens par 90 minutes',
                text='Buts_par_90'
            )
            fig_goals90.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_goals90.update_layout(height=420, showlegend=False)
            st.plotly_chart(fig_goals90, use_container_width=True)

        with col_perf_2:
            fig_assists90 = px.bar(
                position_performance.sort_values('Passes_par_90', ascending=False),
                x='Position',
                y='Passes_par_90',
                color='Passes_par_90',
                color_continuous_scale='Blues',
                title='Passes décisives moyennes par 90 minutes',
                text='Passes_par_90'
            )
            fig_assists90.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_assists90.update_layout(height=420, showlegend=False)
            st.plotly_chart(fig_assists90, use_container_width=True)

        st.markdown("---")

        st.subheader("Temps de jeu et rendement offensif")
        fig_minutes_goals = px.scatter(
            df_filtered,
            x='Minutes',
            y='Buts_par_90',
            color='Position',
            size='Passes_par_90',
            hover_data=['Joueur', 'Équipe', 'Matchs_Joués', 'Buts', 'Passes_Décisives', 'Passes_par_90'],
            title='Minutes jouées vs buts par 90 minutes',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_minutes_goals.update_layout(height=450)
        st.plotly_chart(fig_minutes_goals, use_container_width=True)

        col_scatter_1, col_scatter_2 = st.columns(2)

        with col_scatter_1:
            fig_goals_assists = px.scatter(
                df_filtered,
                x='Buts_par_90',
                y='Passes_par_90',
                size='Minutes_par_Match',
                color='Position',
                hover_data=['Joueur', 'Équipe', 'Matchs_Joués'],
                title='Buts vs passes décisives par 90 minutes',
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig_goals_assists.update_layout(height=420)
            st.plotly_chart(fig_goals_assists, use_container_width=True)

        with col_scatter_2:
            upper_limit = max(int(df_filtered['Matchs_Joués'].max()), 31)
            experience_view = df_filtered.copy()
            experience_view['Niveau_Expérience'] = pd.cut(
                experience_view['Matchs_Joués'],
                bins=[0, 10, 20, 30, upper_limit + 1],
                labels=['Débutant (1-10)', 'Intermédiaire (11-20)', 'Confirmé (21-30)', 'Expert (31+)'],
                right=False,
                include_lowest=True
            )
            fig_experience = px.scatter(
                experience_view,
                x='Matchs_Joués',
                y='Buts_par_90',
                color='Niveau_Expérience',
                size='Passes_par_90',
                hover_data=['Joueur', 'Équipe', 'Position', 'Minutes_par_Match'],
                title="Rendement offensif selon l'expérience",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_experience.update_layout(height=420)
            st.plotly_chart(fig_experience, use_container_width=True)

        st.markdown("---")

        st.subheader("Top 15 contributions offensives (≥ 5 matchs)")
        top_contributions = df_filtered[df_filtered['Matchs_Joués'] >= 5].nlargest(15, 'Buts_plus_Passes_90')

        fig_top_contrib = px.bar(
            top_contributions,
            y='Joueur',
            x='Buts_plus_Passes_90',
            orientation='h',
            color='Buts_plus_Passes_90',
            color_continuous_scale='Teal',
            hover_data=['Équipe', 'Position', 'Matchs_Joués', 'Buts_par_90', 'Passes_par_90'],
            title='Buts + passes par 90 minutes'
        )
        fig_top_contrib.update_layout(yaxis=dict(autorange='reversed'), height=520)
        st.plotly_chart(fig_top_contrib, use_container_width=True)

with tab_leagues:
    st.header("Comparaison des ligues")

    if df_filtered.empty:
        st.write("Aucune donnée à comparer pour les filtres actuels.")
    else:
        st.subheader("Volumes cumulés")
        league_totals = df_filtered.groupby('Ligue')[['Buts', 'Passes_Décisives']].sum().reset_index()
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
                'Passes_Décisives': '#636EFA'
            }
        )
        fig_league_totals.update_layout(height=480, xaxis_title='Ligue', yaxis_title='Volume cumulé')
        st.plotly_chart(fig_league_totals, use_container_width=True)

        st.markdown("---")

        st.subheader("Moyennes par joueur")
        league_means = df_filtered.groupby('Ligue')[['Buts_par_90', 'Passes_par_90']].mean().reset_index()
        league_means = league_means.sort_values('Buts_par_90', ascending=False)
        st.dataframe(league_means.round(3), hide_index=True, width='stretch')

        league_means_long = league_means.melt(id_vars='Ligue', var_name='Indicateur', value_name='Valeur')

        fig_league_means = px.bar(
            league_means_long,
            x='Ligue',
            y='Valeur',
            color='Indicateur',
            barmode='group',
            title='Production moyenne par joueur (par 90 minutes)',
            color_discrete_map={
                'Buts_par_90': '#EF553B',
                'Passes_par_90': '#636EFA'
            }
        )
        fig_league_means.update_layout(height=480, xaxis_title='Ligue', yaxis_title='Valeur moyenne')
        st.plotly_chart(fig_league_means, use_container_width=True)

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
        st.plotly_chart(fig_positions_league, use_container_width=True)

with tab_details:
    st.header("Analyse détaillée des joueurs")

    st.subheader("Recherche et fiche joueur")

    player_names = sorted(df_filtered['Joueur'].unique())
    if player_names:
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
        stat_cols[0].metric("Matchs joués", int(selected_player['Matchs_Joués']))
        stat_cols[1].metric("Buts", int(selected_player['Buts']))
        stat_cols[2].metric("Passes décisives", int(selected_player['Passes_Décisives']))

        ratio_cols = st.columns(3)
        ratio_cols[0].metric("Buts par match", f"{selected_player['Buts_par_Match']:.3f}")
        ratio_cols[1].metric("Passes décisives par match", f"{selected_player['Passes_Déc_par_Match']:.3f}")
        ratio_cols[2].metric("Minutes par match", f"{selected_player['Minutes_par_Match']:.1f}")

        radar_metrics = [
            ('Buts_par_90', 'Buts/90'),
            ('Passes_par_90', 'Passes/90'),
            ('Buts_plus_Passes_90', 'Buts+Passes/90'),
            ('xG_par_90', 'xG/90'),
            ('xAG_par_90', 'xAG/90')
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
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.write("Données insuffisantes pour générer un radar pour ce joueur.")
    else:
        st.write("Aucun joueur ne correspond aux filtres sélectionnés.")

    st.subheader("Comparateur de joueurs")
    if player_names:
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
                    'Joueur', 'Position', 'Équipe', 'Ligue', 'Matchs_Joués', 'Minutes',
                    'Buts', 'Passes_Décisives', 'Buts_par_90', 'Passes_par_90',
                    'Buts_plus_Passes_90', 'xG_par_90', 'xAG_par_90'
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
                    'Buts_par_90': 'Buts/90',
                    'Passes_par_90': 'Passes/90',
                    'Buts_plus_Passes_90': 'Buts+Passes/90',
                    'xG_par_90': 'xG/90',
                    'xAG_par_90': 'xAG/90'
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
                    st.plotly_chart(fig_compare_radar, use_container_width=True)
                else:
                    st.write("Les indicateurs sélectionnés ne permettent pas de générer un radar comparatif.")
        else:
            st.write("Sélectionnez un ou plusieurs joueurs pour lancer la comparaison.")

    st.markdown("---")

    st.subheader("Matrice de corrélation")

    correlation_columns = ['Buts_par_90', 'Passes_par_90', 'Minutes_par_Match', 'Matchs_Joués', 'Âge']
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
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.write("La matrice de corrélation est disponible lorsque des joueurs sont filtrés.")

    st.markdown("---")

    st.subheader("Analyse multi-dimensionnelle")

    if not df_filtered.empty:
        fig_scatter_3d = px.scatter_3d(
            df_filtered,
            x='Buts_par_90',
            y='Passes_par_90',
            z='Minutes_par_Match',
            color='Position',
            size='Matchs_Joués',
            hover_data=['Joueur', 'Équipe', 'Âge'],
            title='Buts, passes décisives et minutes par 90 minutes'
        )
        fig_scatter_3d.update_layout(height=600)
        st.plotly_chart(fig_scatter_3d, use_container_width=True)
    else:
        st.write("L'analyse multi-dimensionnelle nécessite au moins un joueur filtré.")

    st.markdown("---")

    st.subheader("Tableau complet des joueurs filtrés")

    base_columns = [
        'Joueur', 'Âge', 'Équipe', 'Ligue', 'Position', 'Matchs_Joués', 'Minutes',
        'Buts', 'Passes_Décisives', 'Buts_par_Match', 'Passes_Déc_par_Match',
        'Minutes_par_Match', 'Buts_par_90', 'Passes_par_90', 'Buts_plus_Passes_90',
        'xG_par_90', 'xAG_par_90'
    ]
    available_columns = [col for col in base_columns if col in df_filtered.columns]
    display_df = df_filtered[available_columns].copy()

    if not display_df.empty:
        round_columns = [
            'Buts_par_Match', 'Passes_Déc_par_Match', 'Minutes_par_Match',
            'Buts_par_90', 'Passes_par_90', 'Buts_plus_Passes_90', 'xG_par_90', 'xAG_par_90'
        ]
        for column in round_columns:
            if column in display_df.columns:
                display_df[column] = display_df[column].round(3)
        if 'Minutes_par_Match' in display_df.columns:
            display_df['Minutes_par_Match'] = display_df['Minutes_par_Match'].round(1)

        sort_columns = [col for col in ['Buts_plus_Passes_90', 'Buts'] if col in display_df.columns]
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
Comment utiliser ce dashboard :
- Utilisez les filtres dans la barre latérale pour sélectionner les ligues, positions, âges et autres critères.
- Explorez les onglets pour analyser la répartition générale, la performance individuelle et les comparaisons inter-ligues.
- Survolez les graphiques pour obtenir des informations complémentaires (zoom, détails, légendes).
- Téléchargez à tout moment les données filtrées depuis l'onglet Analyse détaillée.

Explication des métriques :
- Buts_par_Match = nombre de buts ÷ matchs joués.
- Passes_Déc_par_Match = passes décisives ÷ matchs joués.
- Buts_par_90 / Passes_par_90 = production ramenée à 90 minutes.
- xG_par_90 = Expected Goals par 90 minutes (buts attendus).
- xAG_par_90 = Expected Assists par 90 minutes (passes attendues).
- Minutes_par_Match = minutes ÷ matchs joués.
""")
