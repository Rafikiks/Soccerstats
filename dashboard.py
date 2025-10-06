import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="⚽ SoccerStats Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚽ Dashboard d'Analyse des Statistiques des Joueurs")
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
    
    return df_cleaned

df = load_data()

st.sidebar.header("🔧 Filtres")

selected_leagues = st.sidebar.multiselect(
    "Sélectionner les Ligues",
    options=df['Ligue'].unique(),
    default=df['Ligue'].unique()
)

positions = st.sidebar.multiselect(
    "Sélectionner les Positions",
    options=sorted(df['Position'].unique()),
    default=sorted(df['Position'].unique())
)

age_range = st.sidebar.slider(
    "Âge des Joueurs",
    int(df['Âge'].min()),
    int(df['Âge'].max()),
    (int(df['Âge'].min()), int(df['Âge'].max()))
)

mp_range = st.sidebar.slider(
    "Nombre de Matchs Joués",
    int(df['Matchs_Joués'].min()),
    int(df['Matchs_Joués'].max()),
    (int(df['Matchs_Joués'].min()), int(df['Matchs_Joués'].max()))
)

min_goals = st.sidebar.slider(
    "Nombre Minimum de Buts",
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
st.sidebar.metric("🎯 Joueurs Sélectionnés", len(df_filtered))

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.metric(
        "👥 Joueurs Sélectionnés",
        len(df_filtered)
    )

with col2:
    st.metric(
        "⚽ Total Buts",
        int(df_filtered['Buts'].sum())
    )

with col3:
    st.metric(
        "🎯 Total Passes Décisives",
        int(df_filtered['Passes_Décisives'].sum())
    )

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'Ensemble",
    "⚽ Buts par Match",
    "🎯 Passes Décisives par Match",
    "⏱️ Temps de Jeu",
    "🔍 Analyse Détaillée"
])

with tab1:
    st.header("📊 Vue d'Ensemble des Statistiques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Buteurs")
        top_scorers = df_filtered.nlargest(10, 'Buts')[['Joueur', 'Équipe', 'Position', 'Buts', 'Matchs_Joués', 'Buts_par_Match']]
        top_scorers['Buts_par_Match'] = top_scorers['Buts_par_Match'].round(3)
        st.dataframe(top_scorers, width='stretch', hide_index=True)
    
    with col2:
        st.subheader("Top 10 Passeurs Décisifs")
        top_assisters = df_filtered.nlargest(10, 'Passes_Décisives')[['Joueur', 'Équipe', 'Position', 'Passes_Décisives', 'Matchs_Joués', 'Passes_Déc_par_Match']]
        top_assisters['Passes_Déc_par_Match'] = top_assisters['Passes_Déc_par_Match'].round(3)
        st.dataframe(top_assisters, width='stretch', hide_index=True)
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        fig = px.pie(
            df_filtered['Position'].value_counts().reset_index(),
            values='count',
            names='Position',
            title='Distribution des Positions',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    with col4:
        comp_stats = df_filtered.groupby('Ligue').agg({
            'Buts': 'sum',
            'Passes_Décisives': 'sum',
            'Minutes': 'sum'
        }).reset_index()
        
        fig = px.bar(
            comp_stats,
            x='Ligue',
            y=['Buts', 'Passes_Décisives'],
            title='Buts et Passes Décisives par Ligue',
            barmode='group',
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')

with tab2:
    st.header("⚽ Analyse des Buts par Match")
    
    st.subheader("Buts par Match selon la Position")
    
    goals_by_pos = df_filtered.groupby('Position').agg({
        'Buts': 'sum',
        'Matchs_Joués': 'sum',
        'Buts_par_Match': 'mean'
    }).reset_index()
    goals_by_pos['Buts_par_Match'] = goals_by_pos['Buts_par_Match'].round(3)
    goals_by_pos = goals_by_pos.sort_values('Buts_par_Match', ascending=False)
    
    fig = px.bar(
        goals_by_pos,
        x='Position',
        y='Buts_par_Match',
        title='Moyenne de Buts par Match par Position',
        color='Buts_par_Match',
        color_continuous_scale='Reds',
        text='Buts_par_Match'
    )
    fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
    fig.update_layout(height=500)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution des Buts par Match")
        fig = px.histogram(
            df_filtered,
            x='Buts_par_Match',
            nbins=30,
            title='Distribution de Buts par Match',
            color_discrete_sequence=['#FF6B6B']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Buts par Match vs Expérience")
        fig = px.scatter(
            df_filtered,
            x='Matchs_Joués',
            y='Buts_par_Match',
            color='Position',
            size='Buts',
            hover_data=['Joueur', 'Équipe', 'Buts', 'Matchs_Joués'],
            title='Relation Matchs Joués vs Buts/Match',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    st.subheader("🏆 Top 20 Joueurs - Buts par Match")
    
    top_gls_per_mp = df_filtered[df_filtered['Matchs_Joués'] >= 5].nlargest(20, 'Buts_par_Match')
    
    fig = px.bar(
        top_gls_per_mp,
        y='Joueur',
        x='Buts_par_Match',
        orientation='h',
        color='Buts_par_Match',
        color_continuous_scale='Reds',
        hover_data=['Équipe', 'Position', 'Buts', 'Matchs_Joués'],
        title='Top 20 Joueurs par Buts/Match (Min 5 matchs)'
    )
    fig.update_layout(yaxis=dict(autorange='reversed'), height=600)
    st.plotly_chart(fig, width='stretch')

with tab3:
    st.header("🎯 Analyse des Passes Décisives par Match")
    
    st.subheader("Passes Décisives par Match selon la Position")
    
    assists_by_pos = df_filtered.groupby('Position').agg({
        'Passes_Décisives': 'sum',
        'Matchs_Joués': 'sum',
        'Passes_Déc_par_Match': 'mean'
    }).reset_index()
    assists_by_pos['Passes_Déc_par_Match'] = assists_by_pos['Passes_Déc_par_Match'].round(3)
    assists_by_pos = assists_by_pos.sort_values('Passes_Déc_par_Match', ascending=False)
    
    fig = px.bar(
        assists_by_pos,
        x='Position',
        y='Passes_Déc_par_Match',
        title='Moyenne de Passes Décisives par Match par Position',
        color='Passes_Déc_par_Match',
        color_continuous_scale='Blues',
        text='Passes_Déc_par_Match'
    )
    fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
    fig.update_layout(height=500)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution des Passes Décisives par Match")
        fig = px.histogram(
            df_filtered,
            x='Passes_Déc_par_Match',
            nbins=30,
            title='Distribution de Passes Décisives par Match',
            color_discrete_sequence=['#4ECDC4']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Passes Décisives par Match vs Expérience")
        fig = px.scatter(
            df_filtered,
            x='Matchs_Joués',
            y='Passes_Déc_par_Match',
            color='Position',
            size='Passes_Décisives',
            hover_data=['Joueur', 'Équipe', 'Passes_Décisives', 'Matchs_Joués'],
            title='Relation Matchs Joués vs Passes Décisives/Match',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    st.subheader("🏆 Top 20 Joueurs - Passes Décisives par Match")
    
    top_ast_per_mp = df_filtered[df_filtered['Matchs_Joués'] >= 5].nlargest(20, 'Passes_Déc_par_Match')
    
    fig = px.bar(
        top_ast_per_mp,
        y='Joueur',
        x='Passes_Déc_par_Match',
        orientation='h',
        color='Passes_Déc_par_Match',
        color_continuous_scale='Blues',
        hover_data=['Équipe', 'Position', 'Passes_Décisives', 'Matchs_Joués'],
        title='Top 20 Joueurs par Passes Décisives/Match (Min 5 matchs)'
    )
    fig.update_layout(yaxis=dict(autorange='reversed'), height=600)
    st.plotly_chart(fig, width='stretch')

with tab4:
    st.header("⏱️ Analyse du Temps de Jeu")
    
    st.subheader("Temps de Jeu selon la Position et l'Expérience")
    
    time_by_pos = df_filtered.groupby('Position').agg({
        'Minutes': 'sum',
        'Matchs_Joués': 'sum',
        'Minutes_par_Match': 'mean',
        'Titularisations': 'sum'
    }).reset_index()
    time_by_pos['Minutes_par_Match'] = time_by_pos['Minutes_par_Match'].round(1)
    time_by_pos['Taux_Titularisation'] = (time_by_pos['Titularisations'] / time_by_pos['Matchs_Joués'] * 100).round(1)
    time_by_pos = time_by_pos.sort_values('Minutes_par_Match', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            time_by_pos,
            x='Position',
            y='Minutes_par_Match',
            title='Minutes Moyennes par Match par Position',
            color='Minutes_par_Match',
            color_continuous_scale='Greens',
            text='Minutes_par_Match'
        )
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig.update_layout(height=500)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        fig = px.bar(
            time_by_pos,
            x='Position',
            y='Taux_Titularisation',
            title='Taux de Titularisation par Position (%)',
            color='Taux_Titularisation',
            color_continuous_scale='Purples',
            text='Taux_Titularisation'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=500)
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    st.subheader("Distribution du Temps de Jeu")
    
    col3, col4 = st.columns(2)
    
    with col3:
        fig = px.histogram(
            df_filtered,
            x='Minutes',
            nbins=30,
            title='Distribution des Minutes Totales',
            color_discrete_sequence=['#95E1D3']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    with col4:
        fig = px.scatter(
            df_filtered,
            x='Matchs_Joués',
            y='Minutes',
            color='Position',
            size='Titularisations',
            hover_data=['Joueur', 'Équipe', 'Minutes', 'Matchs_Joués', 'Titularisations'],
            title='Minutes Totales vs Matchs Joués',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    st.subheader("🏆 Top 20 Joueurs - Temps de Jeu")
    
    top_minutes = df_filtered.nlargest(20, 'Minutes')
    
    fig = px.bar(
        top_minutes,
        y='Joueur',
        x='Minutes',
        orientation='h',
        color='Minutes_par_Match',
        color_continuous_scale='Greens',
        hover_data=['Équipe', 'Position', 'Minutes', 'Matchs_Joués', 'Titularisations'],
        title='Top 20 Joueurs par Minutes Jouées'
    )
    fig.update_layout(yaxis=dict(autorange='reversed'), height=600)
    st.plotly_chart(fig, width='stretch')

with tab5:
    st.header("🔍 Analyse Détaillée des Joueurs")
    
    st.subheader("Matrice de Corrélation : Buts, Passes Décisives et Temps de Jeu")
    
    correlation_data = df_filtered[['Buts_par_Match', 'Passes_Déc_par_Match', 'Minutes_par_Match', 'Matchs_Joués', 'Âge']].corr()
    
    fig = px.imshow(
        correlation_data,
        text_auto='.2f',
        aspect='auto',
        color_continuous_scale='RdBu_r',
        title='Matrice de Corrélation'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    st.subheader("Analyse Multi-Dimensionnelle")
    
    fig = px.scatter_3d(
        df_filtered,
        x='Buts_par_Match',
        y='Passes_Déc_par_Match',
        z='Minutes_par_Match',
        color='Position',
        size='Matchs_Joués',
        hover_data=['Joueur', 'Équipe', 'Âge'],
        title='Analyse 3D : Buts/Match vs Passes Décisives/Match vs Minutes/Match',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    st.subheader("Performance par Position et Expérience")
    
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            perf_by_exp,
            x='Niveau_Expérience',
            y='Buts_par_Match',
            color='Position',
            barmode='group',
            title='Buts/Match par Niveau d\'Expérience et Position',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        fig = px.bar(
            perf_by_exp,
            x='Niveau_Expérience',
            y='Passes_Déc_par_Match',
            color='Position',
            barmode='group',
            title='Passes Décisives/Match par Niveau d\'Expérience et Position',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    st.subheader("📋 Tableau Complet des Joueurs")
    
    display_df = df_filtered[[
        'Joueur', 'Âge', 'Équipe', 'Ligue', 'Position', 'Matchs_Joués', 'Minutes',
        'Buts', 'Buts_par_Match', 'Passes_Décisives', 'Passes_Déc_par_Match', 'Minutes_par_Match'
    ]].copy()
    
    display_df['Buts_par_Match'] = display_df['Buts_par_Match'].round(3)
    display_df['Passes_Déc_par_Match'] = display_df['Passes_Déc_par_Match'].round(3)
    display_df['Minutes_par_Match'] = display_df['Minutes_par_Match'].round(1)
    
    display_df = display_df.sort_values('Buts', ascending=False)
    
    st.dataframe(
        display_df,
        width='stretch',
        hide_index=True,
        height=400
    )
    
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger les données filtrées (CSV)",
        data=csv,
        file_name='joueurs_filtres.csv',
        mime='text/csv',
    )

st.markdown("---")

st.info("""
**💡 Comment utiliser ce dashboard :**
- Utilisez les filtres dans la **barre latérale** pour sélectionner les ligues, positions, âges, etc.
- Explorez les différents **onglets** pour voir les analyses de buts, passes décisives et temps de jeu
- Les graphiques sont **interactifs** : survolez, zoomez, cliquez sur les légendes
- Téléchargez les données filtrées depuis l'onglet "Analyse Détaillée"

**📊 Explication des Métriques :**
- **Buts_par_Match** = Nombre de Buts ÷ Matchs Joués (ex: 0.911 = presque 1 but/match)
- **Passes_Déc_par_Match** = Passes Décisives ÷ Matchs Joués
- **Passe Décisive** = Dernière passe avant un but marqué
""")
