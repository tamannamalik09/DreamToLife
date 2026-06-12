"""
SymbolAgent: detect symbols in the dream text using a knowledge base
of common dream symbols and their themes/meanings.
"""
import json
from pathlib import Path
import re


class SymbolAgent:
    """Loads the symbols DB and matches keywords to detect symbols and themes."""

    def __init__(self):
        base = Path(__file__).resolve().parent.parent
        self.db_path = base / "data" / "symbols.json"
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                self.db = json.load(f)
        except Exception:
            self.db = {}

        self._compile_index()

    def _compile_index(self):
        # Build a list of (symbol, keywords, themes)
        self.index = []
        for symbol, info in self.db.items():
            keywords = info.get("keywords", [])
            themes = info.get("themes", [])
            self.index.append((symbol, [k.lower() for k in keywords], themes))

    def extract(self, text: str):
        """Return (symbols_list, themes_list) found in the text."""
        t = text.lower()
        found = set()
        themes = set()
        for symbol, keywords, sym_themes in self.index:
            for k in keywords:
                if k in t:
                    found.add(symbol)
                    for th in sym_themes:
                        themes.add(th)
                    break

        return sorted(list(found)), sorted(list(themes))
