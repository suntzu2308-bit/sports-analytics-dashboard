"""Interactive portfolio dashboard using synthetic sports results."""
from datetime import date

import pandas as pd
import streamlit as st

from src.analyze import ROOT, aggregate, load_games

st.set_page_config(page_title="Sports Performance | Analytics Portfolio", page_icon="📊", layout="wide")
st.title("Sports Performance Dashboard")
st.caption("Portfolio demonstration · Fabricated games · No proprietary models")

try:
    games = load_games(ROOT / "data/games.csv")
except (OSError, ValueError) as exc:
    st.error(f"Unable to load validated dataset: {exc}")
    st.stop()

teams = sorted({g["home_team"] for g in games} | {g["away_team"] for g in games})
dates = sorted({date.fromisoformat(g["date"]) for g in games})
st.sidebar.header("Filters")
selected_teams = st.sidebar.multiselect("Teams", teams, default=teams)
date_range = st.sidebar.date_input("Game date range", value=(dates[0], dates[-1]), min_value=dates[0], max_value=dates[-1])
if not isinstance(date_range, (list, tuple)) or len(date_range) != 2:
    st.info("Select both start and end dates.")
    st.stop()
start, end = date_range
if start > end:
    st.warning("Start date must be on or before end date.")
    st.stop()

# Filter games by date, then aggregate each team's actual games in the window.
# Team selection controls which aggregated teams are displayed, not which games count.
window_games = [g for g in games if start <= date.fromisoformat(g["date"]) <= end]
records = [r for r in aggregate(window_games) if r["team"] in selected_teams]
if not records:
    st.warning("No team performance data matches these filters.")
    st.stop()

frame = pd.DataFrame(records).sort_values(["win_pct", "point_diff", "team"], ascending=[False, False, True])
total_games = len(window_games)
leader = frame.iloc[0]
a, b, c, d = st.columns(4)
a.metric("Games in date window", f"{total_games}")
b.metric("Teams displayed", f"{len(frame)}")
c.metric("Highest win percentage", f"{leader['win_pct']:.1%}")
d.metric("Leading team", str(leader["team"]))

st.subheader("Team performance")
st.dataframe(frame.rename(columns={
    "team": "Team", "games": "Games", "wins": "Wins", "win_pct": "Win %",
    "avg_scored": "Avg scored", "avg_allowed": "Avg allowed", "point_diff": "Point differential"
}).style.format({"Win %": "{:.1%}", "Avg scored": "{:.2f}", "Avg allowed": "{:.2f}"}),
    use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("Win percentage")
    st.bar_chart(frame.set_index("team")["win_pct"], y_label="Win percentage")
with right:
    st.subheader("Average points per game")
    st.bar_chart(frame.set_index("team")[["avg_scored", "avg_allowed"]], y_label="Points")

st.subheader("Game log (date-filtered)")
st.dataframe(pd.DataFrame(window_games).rename(columns={
    "game_id": "Game ID", "date": "Date", "home_team": "Home", "away_team": "Away",
    "home_score": "Home score", "away_score": "Away score"
}), use_container_width=True, hide_index=True)

st.download_button("Download filtered team KPIs (CSV)",
                   frame.to_csv(index=False).encode("utf-8"),
                   file_name="synthetic_team_kpis.csv", mime="text/csv")
st.caption("Metrics are descriptive only. Eight fabricated games are insufficient for predictive or betting claims. "
           "Team filtering does not remove opponents from team-level statistics.")
