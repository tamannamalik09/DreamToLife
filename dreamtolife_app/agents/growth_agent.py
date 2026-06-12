"""
GrowthAgent: track recurring symbols, emotions and themes across multiple
dreams and present growth insights.
"""
import json
from pathlib import Path
from collections import Counter


class GrowthAgent:
    """Provides utilities to analyze the saved dream journal over time."""

    def __init__(self):
        self.journal_path = Path(__file__).resolve().parent.parent.parent / "dream_journal.json"

    def recurring_themes(self, journal_path: str = None) -> dict:
        path = Path(journal_path) if journal_path else self.journal_path
        try:
            with open(path, "r", encoding="utf-8") as f:
                entries = json.load(f)
        except Exception:
            entries = []

        counter = Counter()
        for e in entries:
            for t in e.get("themes", []):
                counter[t] += 1
            for s in e.get("symbols", []):
                counter[s] += 1

        return dict(counter.most_common())

    def summarize_from_text(self, dream_text: str, symbols: list, emotions: dict) -> str:
        # Lightweight insight generator: detect if dream contains repeated symbols
        insight = []
        if symbols:
            insight.append(f"You are revisiting {', '.join(symbols)}; this may indicate a recurring concern or theme.")
        if emotions:
            primary = max(emotions, key=emotions.get)
            insight.append(f"The dominant emotion appears to be {primary}. Consider exploring that feeling in waking life.")
        if not insight:
            return "No strong recurring signals detected — keep observing."
        return " ".join(insight)

    def generate_growth_report(self, journal_path: str = None) -> str:
        path = Path(journal_path) if journal_path else self.journal_path
        try:
            with open(path, "r", encoding="utf-8") as f:
                entries = json.load(f)
        except Exception:
            entries = []

        total = len(entries)
        recurring = self.recurring_themes(path)

        lines = []
        lines.append("\n🌱 GROWTH REPORT")
        lines.append(f"Dreams logged: {total}")
        if recurring:
            lines.append("Top recurring themes/symbols:")
            for k, v in list(recurring.items())[:10]:
                lines.append(f" - {k}: {v} times")
        else:
            lines.append("No recurring themes found yet.")

        return "\n".join(lines)
