"""
DreamJournal: simple JSON-backed storage for dream analyses.

Stores entries with: date, dream_text, emotions, symbols, themes, actions,
scorecard, and a printable report text.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict


class DreamJournal:
    """Manage reading/writing the `dream_journal.json` file."""

    def __init__(self, path: str = None):
        # Default file at workspace root
        if path:
            self.path = Path(path)
        else:
            self.path = Path(__file__).resolve().parent.parent / "dream_journal.json"
        # Ensure file exists
        if not self.path.exists():
            try:
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2)
            except Exception:
                pass

    def add_entry(self, report: Dict):
        try:
            entries = self.get_all_entries()
            entry = report.copy()
            # Ensure there's a timestamp
            entry.setdefault("date", datetime.utcnow().isoformat())
            entries.append(entry)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def get_all_entries(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
