# SoccerStats

Analysis and dashboarding toolkit for the 2024‑2025 season of the top five European leagues. The project ingests the public dataset `top5-players24-25.csv` (2 852 players, 37 variables) and provides:

- a reproducible Python workflow (`analysis_young_players.py`) tailored to scouting players aged 21 or younger;
- an interactive Streamlit dashboard (`dashboard.py`) for exploring the full population (any age) across positions, leagues and clubs.

## 1. Repository Layout

```
SoccerStats/
├── analysis_young_players.py     # End-to-end analysis script focused on young players
├── dashboard.py                  # Streamlit application (multi-tab analytics)
├── DASHBOARD_GUIDE.md            # Detailed usage manual for the dashboard
├── requirements.txt              # Python dependencies
├── top5-players24-25.csv         # Full dataset (input)
├── analyse jeunes joueurs.csv    # Exported table from the young-players workflow
├── top 30 jeunes joueurs.csv     # Young players ranked by goals + assists
├── statistiques roles.csv        # Aggregated statistics per inferred role
└── README.md                     # Project overview (this file)
```

## 2. Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# .\venv\Scripts\activate      # Windows PowerShell
pip install -r requirements.txt
```

## 3. Running the Analyses

### 3.1 Scripted pipeline (≤ 21 ans)

```bash
python analysis_young_players.py
```

Produces three CSV artefacts at the project root:

- `analyse jeunes joueurs.csv` – complete record of qualified players with advanced metrics and inferred roles (Finisher, Defender, Playmaker).
- `top 30 jeunes joueurs.csv` – ranking by total goals plus assists.
- `statistiques roles.csv` – descriptive statistics per role cluster.

The script handles data cleaning, feature engineering (xG, xAG, progressive actions), exploratory charts saved in the `figures` directory (created on the fly) and a basic clustering workflow (PCA + k-means).

### 3.2 Interactive dashboard

```bash
streamlit run dashboard.py
```

The app opens on http://localhost:8501 and exposes four tabs:

1. **Vue d'ensemble** – positional and national distributions, leaderboard tables, aggregated indicators.
2. **Analyse individuelle** – per-position averages, scatterplots relating workload to offensive output, top contributions per 90 minutes.
3. **Comparaison des ligues** – tables and bar charts comparing goals and assists totals/averages plus squad composition by position.
4. **Analyse détaillée** – player search, comparative radar, multi-player comparator, correlation matrix, 3D scatter and exportable table.

Refer to `DASHBOARD_GUIDE.md` for screenshots, filter descriptions and customisation hints.

## 4. Dataset Overview

Source file: `top5-players24-25.csv`

- Coverage: Premier League, La Liga, Serie A, Bundesliga, Ligue 1.
- Key columns: `Player`, `Nation`, `Pos`, `Squad`, `Comp`, `Age`, `MP`, `Starts`, `Min`, `Gls`, `Ast`, `G+A`, `xG`, `xAG`, `PrgP`, `PrgC`, `PrgR`, disciplinary data.
- Derived metrics in project outputs: ratios per match, per 90 minutes, cumulative contributions, expected metrics, progressive actions, role clustering labels.

## 5. Key Indicators (definitions)

| Metric                          | Description                                                                         |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| `Buts_par_Match`                | Goals divided by matches played (`Gls / MP`).                                       |
| `Passes_Déc_par_Match`          | Assists divided by matches played (`Ast / MP`).                                     |
| `Minutes_par_Match`             | Minutes divided by matches played (`Min / MP`).                                     |
| `Buts_par_90` / `Passes_par_90` | Goals or assists normalised per 90 minutes (`Gls / 90s`, `Ast / 90s`).              |
| `Buts_plus_Passes_90`           | Sum of goals and assists per 90 minutes.                                            |
| `xG_par_90`, `xAG_par_90`       | Expected goals/assists per 90 minutes.                                              |
| `Matchs_90`                     | Equivalent full matches (`90s`).                                                    |
| `Niveau_Expérience`             | Categorisation based on matches played (Débutant, Intermédiaire, Confirmé, Expert). |

## 6. Customisation Points

- Modify age threshold or minimum match logic inside `analysis_young_players.py` to target different cohorts.
- Extend the dashboard filters or charts by editing `dashboard.py` (for example adjust Plotly colour sequences or add new derived metrics in `load_data`).
- Replace `top5-players24-25.csv` with another export: update the mapping dictionaries for nations/positions if new values appear.

## 7. Troubleshooting

| Symptom                          | Resolution                                                                                                            |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Streamlit refuses to start       | Ensure the virtual environment is active and dependencies are installed; run `pip install -r requirements.txt` again. |
| Port 8501 already in use         | Launch `streamlit run dashboard.py --server.port 8502`.                                                               |
| Empty dashboard views            | Check that filters are not overly restrictive; inspect the CSV for missing columns.                                   |
| Analysis script fails on imports | Confirm the interpreter uses the virtual environment (run `which python` / `where python`).                           |

## 8. Credits

Dataset exploration adapted from the Kaggle work of dzulfikrialwi and extended by Rafikiks for scouting and dashboard purposes. Use the material for educational or analytical objectives; no licence warranty is provided.
