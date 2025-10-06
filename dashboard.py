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
    df_cleaned['Buts_par_Match'] = df_cleaned['Gls'] / df_cleaned['MP']
    df_cleaned['Passes_Dec_par_Match'] = df_cleaned['Ast'] / df_cleaned['MP']
    df_cleaned['Minutes_par_Match'] = df_cleaned['Min'] / df_cleaned['MP']

    column_names = {
        'Player': 'Joueur',
        'Nation': 'Nationalité',
        'Squad': 'Équipe',
        'Comp': 'Ligue',
        'Age': 'Âge',
        'Pos': 'Position',
        'MP': 'Matchs_Joués',
        'Starts': 'Titularisations',
        'Min': 'Minutes',
        'Gls': 'Buts',
        'Ast': 'Passes_Décisives',
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

    return df_cleaned


df = load_data()

st.sidebar.header("Filtres")

selected_leagues = st.sidebar.multiselect(
    "Sélectionner les ligues",
    options=df['Ligue'].unique(),
    default=df['Ligue'].unique()
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

tab_overview, tab_positions, tab_performance, tab_details = st.tabs([
    "Vue d'ensemble",
    "Positions et nations",
    "Performance en match",
    "Analyse détaillée"
])

with tab_overview:
    st.header("Vue d'ensemble des statistiques")

    col_overview_1, col_overview_2 = st.columns(2)

    with col_overview_1:
        st.subheader("Top 10 buteurs")
        top_scorers = df_filtered.nlargest(10, 'Buts')[
            ['Joueur', 'Nationalité', 'Équipe', 'Position', 'Buts', 'Matchs_Joués', 'Buts_par_Match']
        ]
        if not top_scorers.empty:
            top_scorers['Buts_par_Match'] = top_scorers['Buts_par_Match'].round(3)
        st.dataframe(top_scorers, width='stretch', hide_index=True)

    with col_overview_2:
        st.subheader("Top 10 passeurs décisifs")
        top_assisters = df_filtered.nlargest(10, 'Passes_Décisives')[
            ['Joueur', 'Nationalité', 'Équipe', 'Position', 'Passes_Décisives', 'Matchs_Joués', 'Passes_Déc_par_Match']
        ]
        if not top_assisters.empty:
            top_assisters['Passes_Déc_par_Match'] = top_assisters['Passes_Déc_par_Match'].round(3)
        st.dataframe(top_assisters, width='stretch', hide_index=True)

    st.markdown("---")

    st.subheader("Indicateurs globaux")
    if not df_filtered.empty:
        col_g1, col_g2, col_g3 = st.columns(3)
        col_g1.metric("Buts par match moyen", f"{df_filtered['Buts_par_Match'].mean():.2f}")
        col_g2.metric("Passes décisives par match moyennes", f"{df_filtered['Passes_Déc_par_Match'].mean():.2f}")
        col_g3.metric("Minutes par match moyennes", f"{df_filtered['Minutes_par_Match'].mean():.1f}")
    else:
        st.write("Aucun joueur ne correspond aux filtres sélectionnés.")

with tab_positions:
    st.header("Distribution par position et nation")

    st.subheader("Nombre de joueurs par position")

    position_counts = df_filtered['Position'].value_counts().reset_index()
    position_counts.columns = ['Position', 'Nombre']

    col_pos_1, col_pos_2 = st.columns([2, 1])

    with col_pos_1:
        fig_positions = px.bar(
            position_counts,
            x='Position',
            y='Nombre',
            title='Distribution des joueurs par position',
            color='Nombre',
            color_continuous_scale='Viridis',
            text='Nombre'
        )
        fig_positions.update_traces(texttemplate='%{text}', textposition='outside')
        fig_positions.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_positions, use_container_width=True)

    with col_pos_2:
        fig_positions_pie = px.pie(
            position_counts,
            values='Nombre',
            names='Position',
            title='Répartition en pourcentage',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_positions_pie.update_layout(height=500)
        st.plotly_chart(fig_positions_pie, use_container_width=True)

    st.markdown("---")

    st.subheader("Nombre de joueurs par nation")

    nation_counts = df_filtered['Nationalité'].value_counts().head(20).reset_index()
    nation_counts.columns = ['Nationalité', 'Nombre']

    col_nat_1, col_nat_2 = st.columns([3, 1])

    with col_nat_1:
        fig_nations = px.bar(
            nation_counts,
            x='Nombre',
            y='Nationalité',
            orientation='h',
            title='Top 20 nations avec le plus de joueurs',
            color='Nombre',
            color_continuous_scale='Blues',
            text='Nombre'
        )
        fig_nations.update_traces(texttemplate='%{text}', textposition='outside')
        fig_nations.update_layout(height=700, yaxis=dict(autorange='reversed'), showlegend=False)
        st.plotly_chart(fig_nations, use_container_width=True)

    with col_nat_2:
        st.markdown("### Top 10 nations")
        top_10_nations = df_filtered['Nationalité'].value_counts().head(10)
        for idx, (nation, count) in enumerate(top_10_nations.items(), 1):
            st.metric(
                f"{idx}. {nation}",
                f"{count} joueurs"
            )

    st.markdown("---")

    st.subheader("Statistiques globales")

    col_global_1, col_global_2, col_global_3, col_global_4 = st.columns(4)

    with col_global_1:
        st.metric("Total positions", df_filtered['Position'].nunique())

    with col_global_2:
        st.metric("Total nations", df_filtered['Nationalité'].nunique())

    with col_global_3:
        st.metric("Total équipes", df_filtered['Équipe'].nunique())

    with col_global_4:
        st.metric("Total ligues", df_filtered['Ligue'].nunique())

    st.markdown("---")

    st.subheader("Répartition des nationalités par position")

    top_10_nations_index = df_filtered['Nationalité'].value_counts().head(10).index
    df_top_nations = df_filtered[df_filtered['Nationalité'].isin(top_10_nations_index)]

    position_nation_data = df_top_nations.groupby(['Position', 'Nationalité']).size().reset_index(name='Nombre')

    fig_position_nation = px.bar(
        position_nation_data,
        x='Position',
        y='Nombre',
        color='Nationalité',
        title='Répartition des top 10 nationalités par position',
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Set3,
        text='Nombre'
    )
    fig_position_nation.update_traces(texttemplate='%{text}', textposition='outside')
    fig_position_nation.update_layout(height=600, xaxis_title='Position', yaxis_title='Nombre de joueurs')
    st.plotly_chart(fig_position_nation, use_container_width=True)

    st.markdown("---")

    col_choice_pos, col_choice_nat = st.columns(2)

    with col_choice_pos:
        st.subheader("Top 5 nationalités par position")
        position_choice = st.selectbox(
            "Choisir une position",
            options=sorted(df_filtered['Position'].unique())
        )
        position_data = df_filtered[df_filtered['Position'] == position_choice]
        top_nations_for_pos = position_data['Nationalité'].value_counts().head(5).reset_index()
        top_nations_for_pos.columns = ['Nationalité', 'Nombre']

        fig_top_nations_pos = px.bar(
            top_nations_for_pos,
            x='Nationalité',
            y='Nombre',
            title=f'Top 5 nationalités pour {position_choice}',
            color='Nombre',
            color_continuous_scale='Blues',
            text='Nombre'
        )
        fig_top_nations_pos.update_traces(texttemplate='%{text}', textposition='outside')
        fig_top_nations_pos.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_top_nations_pos, use_container_width=True)

    with col_choice_nat:
        st.subheader("Positions par nationalité")
        nation_choice = st.selectbox(
            "Choisir une nationalité",
            options=sorted(df_filtered['Nationalité'].unique())
        )
        nation_data = df_filtered[df_filtered['Nationalité'] == nation_choice]
        position_dist = nation_data['Position'].value_counts().reset_index()
        position_dist.columns = ['Position', 'Nombre']

        fig_position_dist = px.pie(
            position_dist,
            values='Nombre',
            names='Position',
            title=f'Distribution des positions pour {nation_choice}',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_position_dist.update_layout(height=400)
        st.plotly_chart(fig_position_dist, use_container_width=True)

with tab_performance:
    st.header("Performance en match")

    st.subheader("Buts par match selon la position")

    goals_by_pos = df_filtered.groupby('Position').agg({
        'Buts': 'sum',
        'Matchs_Joués': 'sum',
        'Buts_par_Match': 'mean'
    }).reset_index()
    goals_by_pos['Buts_par_Match'] = goals_by_pos['Buts_par_Match'].round(3)
    goals_by_pos = goals_by_pos.sort_values('Buts_par_Match', ascending=False)

    fig_goals_by_pos = px.bar(
        goals_by_pos,
        x='Position',
        y='Buts_par_Match',
        title='Moyenne de buts par match par position',
        color='Buts_par_Match',
        color_continuous_scale='Reds',
        text='Buts_par_Match'
    )
    fig_goals_by_pos.update_traces(texttemplate='%{text:.3f}', textposition='outside')
    fig_goals_by_pos.update_layout(height=500)
    st.plotly_chart(fig_goals_by_pos, use_container_width=True)

    st.markdown("### Répartition des buts par match")

    col_goals_1, col_goals_2 = st.columns(2)

    with col_goals_1:
        fig_goals_hist = px.histogram(
            df_filtered,
            x='Buts_par_Match',
            nbins=30,
            title='Distribution de buts par match',
            color_discrete_sequence=['#FF6B6B']
        )
        fig_goals_hist.update_layout(height=400)
        st.plotly_chart(fig_goals_hist, use_container_width=True)

    with col_goals_2:
        fig_goals_scatter = px.scatter(
            df_filtered,
            x='Matchs_Joués',
            y='Buts_par_Match',
            color='Position',
            size='Buts',
            hover_data=['Joueur', 'Équipe', 'Buts', 'Matchs_Joués'],
            title='Relation matchs joués et buts par match',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_goals_scatter.update_layout(height=400)
        st.plotly_chart(fig_goals_scatter, use_container_width=True)

    st.markdown("### Top 20 joueurs par buts par match")

    top_gls_per_mp = df_filtered[df_filtered['Matchs_Joués'] >= 5].nlargest(20, 'Buts_par_Match')

    fig_top_goals = px.bar(
        top_gls_per_mp,
        y='Joueur',
        x='Buts_par_Match',
        orientation='h',
        color='Buts_par_Match',
        color_continuous_scale='Reds',
        hover_data=['Équipe', 'Position', 'Buts', 'Matchs_Joués'],
        title='Top 20 joueurs par buts par match (minimum 5 matchs)'
    )
    fig_top_goals.update_layout(yaxis=dict(autorange='reversed'), height=600)
    st.plotly_chart(fig_top_goals, use_container_width=True)

    st.markdown("---")

    st.subheader("Passes décisives par match selon la position")

    assists_by_pos = df_filtered.groupby('Position').agg({
        'Passes_Décisives': 'sum',
        'Matchs_Joués': 'sum',
        'Passes_Déc_par_Match': 'mean'
    }).reset_index()
    assists_by_pos['Passes_Déc_par_Match'] = assists_by_pos['Passes_Déc_par_Match'].round(3)
    assists_by_pos = assists_by_pos.sort_values('Passes_Déc_par_Match', ascending=False)

    fig_assists_by_pos = px.bar(
        assists_by_pos,
        x='Position',
        y='Passes_Déc_par_Match',
        title='Moyenne de passes décisives par match par position',
        color='Passes_Déc_par_Match',
        color_continuous_scale='Blues',
        text='Passes_Déc_par_Match'
    )
    fig_assists_by_pos.update_traces(texttemplate='%{text:.3f}', textposition='outside')
    fig_assists_by_pos.update_layout(height=500)
    st.plotly_chart(fig_assists_by_pos, use_container_width=True)

    st.markdown("### Répartition des passes décisives par match")

    col_assists_1, col_assists_2 = st.columns(2)

    with col_assists_1:
        fig_assists_hist = px.histogram(
            df_filtered,
            x='Passes_Déc_par_Match',
            nbins=30,
            title='Distribution de passes décisives par match',
            color_discrete_sequence=['#4ECDC4']
        )
        fig_assists_hist.update_layout(height=400)
        st.plotly_chart(fig_assists_hist, use_container_width=True)

    with col_assists_2:
        fig_assists_scatter = px.scatter(
            df_filtered,
            x='Matchs_Joués',
            y='Passes_Déc_par_Match',
            color='Position',
            size='Passes_Décisives',
            hover_data=['Joueur', 'Équipe', 'Passes_Décisives', 'Matchs_Joués'],
            title='Relation matchs joués et passes décisives par match',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_assists_scatter.update_layout(height=400)
        st.plotly_chart(fig_assists_scatter, use_container_width=True)

    st.markdown("### Top 20 joueurs par passes décisives par match")

    top_ast_per_mp = df_filtered[df_filtered['Matchs_Joués'] >= 5].nlargest(20, 'Passes_Déc_par_Match')

    fig_top_assists = px.bar(
        top_ast_per_mp,
        y='Joueur',
        x='Passes_Déc_par_Match',
        orientation='h',
        color='Passes_Déc_par_Match',
        color_continuous_scale='Blues',
        hover_data=['Équipe', 'Position', 'Passes_Décisives', 'Matchs_Joués'],
        title='Top 20 joueurs par passes décisives par match (minimum 5 matchs)'
    )
    fig_top_assists.update_layout(yaxis=dict(autorange='reversed'), height=600)
    st.plotly_chart(fig_top_assists, use_container_width=True)

    st.markdown("---")

    st.subheader("Temps de jeu")

    col_minutes_1, col_minutes_2 = st.columns(2)

    with col_minutes_1:
        fig_minutes_hist = px.histogram(
            df_filtered,
            x='Minutes',
            nbins=30,
            title='Distribution des minutes totales',
            color_discrete_sequence=['#95E1D3']
        )
        fig_minutes_hist.update_layout(height=400)
        st.plotly_chart(fig_minutes_hist, use_container_width=True)

    with col_minutes_2:
        fig_minutes_scatter = px.scatter(
            df_filtered,
            x='Matchs_Joués',
            y='Minutes',
            color='Position',
            size='Titularisations',
            hover_data=['Joueur', 'Équipe', 'Minutes', 'Matchs_Joués', 'Titularisations'],
            title='Minutes totales et matchs joués',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_minutes_scatter.update_layout(height=400)
        st.plotly_chart(fig_minutes_scatter, use_container_width=True)

    st.markdown("### Top 20 joueurs par minutes jouées")

    top_minutes = df_filtered.nlargest(20, 'Minutes')

    fig_top_minutes = px.bar(
        top_minutes,
        y='Joueur',
        x='Minutes',
        orientation='h',
        color='Minutes_par_Match',
        color_continuous_scale='Greens',
        hover_data=['Équipe', 'Position', 'Minutes', 'Matchs_Joués', 'Titularisations'],
        title='Top 20 joueurs par minutes jouées'
    )
    fig_top_minutes.update_layout(yaxis=dict(autorange='reversed'), height=600)
    st.plotly_chart(fig_top_minutes, use_container_width=True)

with tab_details:
    st.header("Analyse détaillée des joueurs")

    st.subheader("Recherche et fiche joueur")

    player_names = sorted(df_filtered['Joueur'].unique())
    if player_names:
        search_name = st.text_input(
            "Rechercher un joueur",
            placeholder="Saisir une partie du nom",
            key="player_search"
        )
        if search_name:
            filtered_player_names = [name for name in player_names if search_name.lower() in name.lower()]
        else:
            filtered_player_names = player_names

        if filtered_player_names:
            player_choice = st.selectbox(
                "Sélectionner un joueur",
                options=filtered_player_names,
                key="player_choice"
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
        else:
            st.warning("Aucun joueur ne correspond à cette recherche.")
    else:
        st.write("Aucun joueur ne correspond aux filtres sélectionnés.")

    st.markdown("---")

    st.subheader("Matrice de corrélation")

    correlation_columns = ['Buts_par_Match', 'Passes_Déc_par_Match', 'Minutes_par_Match', 'Matchs_Joués', 'Âge']
    correlation_data = df_filtered[correlation_columns].corr() if not df_filtered.empty else pd.DataFrame(columns=correlation_columns)

    if not correlation_data.empty:
        fig_corr = px.imshow(
            correlation_data,
            text_auto='.2f',
            aspect='auto',
            color_continuous_scale='RdBu_r',
            title='Matrice de corrélation des indicateurs clés'
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
            x='Buts_par_Match',
            y='Passes_Déc_par_Match',
            z='Minutes_par_Match',
            color='Position',
            size='Matchs_Joués',
            hover_data=['Joueur', 'Équipe', 'Âge'],
            title='Buts, passes décisives et minutes par match'
        )
        fig_scatter_3d.update_layout(height=600)
        st.plotly_chart(fig_scatter_3d, use_container_width=True)
    else:
        st.write("L'analyse multi-dimensionnelle nécessite au moins un joueur filtré.")

    st.markdown("---")

    st.subheader("Performance par position et expérience")

    if not df_filtered.empty:
        df_filtered_copy = df_filtered.copy()
        df_filtered_copy['Niveau_Expérience'] = pd.cut(
            df_filtered_copy['Matchs_Joués'],
            bins=[0, 10, 20, 30, 100],
            labels=['Débutant (1-10)', 'Intermédiaire (11-20)', 'Confirmé (21-30)', 'Expert (31+)']
        )

        perf_by_exp = df_filtered_copy.groupby(['Position', 'Niveau_Expérience'], observed=True).agg({
            'Buts_par_Match': 'mean',
            'Passes_Déc_par_Match': 'mean',
            'Minutes_par_Match': 'mean'
        }).reset_index()

        col_perf_exp_1, col_perf_exp_2 = st.columns(2)

        with col_perf_exp_1:
            fig_perf_goals = px.bar(
                perf_by_exp,
                x='Niveau_Expérience',
                y='Buts_par_Match',
                color='Position',
                barmode='group',
                title="Buts par match par niveau d'expérience et position",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_perf_goals.update_layout(height=500)
            st.plotly_chart(fig_perf_goals, use_container_width=True)

        with col_perf_exp_2:
            fig_perf_assists = px.bar(
                perf_by_exp,
                x='Niveau_Expérience',
                y='Passes_Déc_par_Match',
                color='Position',
                barmode='group',
                title="Passes décisives par match par niveau d'expérience et position",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_perf_assists.update_layout(height=500)
            st.plotly_chart(fig_perf_assists, use_container_width=True)
    else:
        st.write("Les graphiques d'expérience nécessitent au moins un joueur filtré.")

    st.markdown("---")

    st.subheader("Tableau complet des joueurs filtrés")

    display_df = df_filtered[[
        'Joueur', 'Âge', 'Équipe', 'Ligue', 'Position', 'Matchs_Joués', 'Minutes',
        'Buts', 'Buts_par_Match', 'Passes_Décisives', 'Passes_Déc_par_Match', 'Minutes_par_Match'
    ]].copy()

    if not display_df.empty:
        display_df['Buts_par_Match'] = display_df['Buts_par_Match'].round(3)
        display_df['Passes_Déc_par_Match'] = display_df['Passes_Déc_par_Match'].round(3)
        display_df['Minutes_par_Match'] = display_df['Minutes_par_Match'].round(1)
        display_df = display_df.sort_values('Buts', ascending=False)

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
- Explorez les onglets pour analyser la distribution des postes, la performance en match et les détails individuels.
- Survolez les graphiques pour obtenir des informations complémentaires (zoom, détails, légendes).
- Téléchargez à tout moment les données filtrées depuis l'onglet Analyse détaillée.

Explication des métriques :
- Buts_par_Match = nombre de buts ÷ matchs joués.
- Passes_Déc_par_Match = passes décisives ÷ matchs joués.
- Minutes_par_Match = minutes ÷ matchs joués.
""")
