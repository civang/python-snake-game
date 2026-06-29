import tempfile
import unittest
from pathlib import Path

from game_utils import get_difficulty_fps, load_high_score, save_high_score


class GameFeatureTests(unittest.TestCase):
    def test_get_difficulty_fps_defaults_to_medium(self):
        self.assertEqual(get_difficulty_fps("medium"), 10)
        self.assertEqual(get_difficulty_fps("unknown"), 10)

    def test_high_score_persistence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            high_score_path = Path(temp_dir) / "highscore.txt"
            self.assertEqual(load_high_score(high_score_path), 0)

            save_high_score(12, high_score_path)
            self.assertEqual(load_high_score(high_score_path), 12)

            save_high_score(8, high_score_path)
            self.assertEqual(load_high_score(high_score_path), 12)


if __name__ == "__main__":
    unittest.main()
