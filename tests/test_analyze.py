import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyze import ROOT, aggregate, load_games

class AnalyticsTests(unittest.TestCase):
    def test_sample_game_count(self):
        self.assertEqual(len(load_games(ROOT / "data/games.csv")), 8)

    def test_aggregate_game_count(self):
        rows = aggregate(load_games(ROOT / "data/games.csv"))
        self.assertEqual(sum(r["games"] for r in rows), 16)
        self.assertTrue(all(0 <= r["win_pct"] <= 1 for r in rows))

    def test_known_team_kpis(self):
        rows = {r["team"]: r for r in aggregate(load_games(ROOT / "data/games.csv"))}
        self.assertEqual(rows["Falcons"]["wins"], 4)
        self.assertEqual(rows["Falcons"]["games"], 4)
        self.assertEqual(rows["Falcons"]["win_pct"], 1.0)
        self.assertEqual(rows["Bears"]["wins"], 0)

    def test_duplicate_id_rejected(self):
        original = (ROOT / "data/games.csv").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "games.csv"
            lines = original.splitlines()
            path.write_text(original + lines[1] + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate game ID"):
                load_games(path)

    def test_self_matchup_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "games.csv"
            path.write_text("game_id,date,home_team,away_team,home_score,away_score\n"
                            "X1,2026-01-01,Falcons,Falcons,2,1\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Team cannot play itself"):
                load_games(path)

    def test_empty_aggregate(self):
        self.assertEqual(aggregate([]), [])

if __name__ == "__main__":
    unittest.main()
