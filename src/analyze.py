"""Validate synthetic games and generate reproducible team KPI reports."""
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_games(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    seen = set()
    for row in rows:
        if not all(row.values()):
            raise ValueError("Missing game field")
        if row["game_id"] in seen:
            raise ValueError("Duplicate game ID")
        seen.add(row["game_id"])
        date.fromisoformat(row["date"])
        if row["home_team"] == row["away_team"]:
            raise ValueError("Team cannot play itself")
        for field in ("home_score", "away_score"):
            if not row[field].isdigit():
                raise ValueError("Score must be a nonnegative integer")
            row[field] = int(row[field])
    return rows

def aggregate(games):
    stats = defaultdict(lambda: {"games": 0, "wins": 0, "scored": 0, "allowed": 0})
    for game in games:
        for side, other in (("home", "away"), ("away", "home")):
            record = stats[game[side + "_team"]]
            scored, allowed = game[side + "_score"], game[other + "_score"]
            record["games"] += 1
            record["wins"] += int(scored > allowed)
            record["scored"] += scored
            record["allowed"] += allowed
    return [{"team": team, "games": s["games"], "wins": s["wins"],
             "win_pct": round(s["wins"] / s["games"], 3),
             "avg_scored": round(s["scored"] / s["games"], 2),
             "avg_allowed": round(s["allowed"] / s["games"], 2),
             "point_diff": s["scored"] - s["allowed"]}
            for team, s in sorted(stats.items())]

def write_chart(rows, path):
    import html
    bars = []
    for index, row in enumerate(rows):
        y = 55 + index * 50
        width = row["win_pct"] * 400
        team = html.escape(row["team"])
        bars.append(f'<text x="10" y="{y+18}">{team}</text><rect x="110" y="{y}" width="{width:.1f}" height="25" fill="#2878a5"/><text x="{120+width:.1f}" y="{y+18}">{row["win_pct"]:.1%}</text>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="650" height="' + str(90+50*len(rows)) + '"><text x="10" y="25" font-size="20">Synthetic team win percentage</text>' + ''.join(bars) + '</svg>'
    path.write_text(svg, encoding="utf-8")

def main():
    rows = aggregate(load_games(ROOT / "data/games.csv"))
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    with (output / "team_kpis.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    write_chart(rows, output / "kpi_chart.svg")
    for row in rows:
        print(row)

if __name__ == "__main__":
    main()
