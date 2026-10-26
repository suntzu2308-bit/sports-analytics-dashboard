import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyze import ROOT, aggregate, load_games

class SQLParityTests(unittest.TestCase):
    def test_kpis_match(self):
        games = load_games(ROOT / "data/games.csv")
        db = sqlite3.connect(":memory:")
        try:
            db.execute("CREATE TABLE games (game_id TEXT, date TEXT, home_team TEXT, away_team TEXT, home_score INTEGER, away_score INTEGER)")
            db.executemany("INSERT INTO games VALUES (:game_id,:date,:home_team,:away_team,:home_score,:away_score)", games)
            sql = (ROOT / "sql/kpis.sql").read_text(encoding="utf-8")
            fields = ["team", "games", "wins", "win_pct", "avg_scored", "avg_allowed", "point_diff"]
            actual = {row[0]: dict(zip(fields, row)) for row in db.execute(sql)}
            expected = {row["team"]: row for row in aggregate(games)}
            self.assertEqual(actual, expected)
        finally:
            db.close()
