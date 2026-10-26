import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyze import load_games, aggregate, ROOT

class AnalyticsTests(unittest.TestCase):
    def test_sample_game_count(self):
        self.assertEqual(len(load_games(ROOT / "data/games.csv")), 8)

    def test_aggregate_game_count(self):
        rows = aggregate(load_games(ROOT / "data/games.csv"))
        self.assertEqual(sum(r["games"] for r in rows), 16)
        self.assertTrue(all(0 <= r["win_pct"] <= 1 for r in rows))

if __name__ == "__main__":
    unittest.main()
