from pathlib import Path

from settings import HIGH_SCORE_FILE


def get_difficulty_fps(difficulty_name):
    difficulty_map = {
        "easy": 8,
        "medium": 10,
        "hard": 14,
    }
    return difficulty_map.get(difficulty_name.lower(), difficulty_map["medium"])


def load_high_score(path=None):
    if path is None:
        path = Path(__file__).resolve().parent / HIGH_SCORE_FILE
    if not path.exists():
        return 0
    try:
        return int(path.read_text(encoding="utf-8").strip() or 0)
    except ValueError:
        return 0


def save_high_score(score, path=None):
    if path is None:
        path = Path(__file__).resolve().parent / HIGH_SCORE_FILE
    current_high_score = load_high_score(path)
    if score > current_high_score:
        path.write_text(str(score), encoding="utf-8")


def get_pause_message(paused):
    return "Press C to continue" if paused else "Press P to pause"
