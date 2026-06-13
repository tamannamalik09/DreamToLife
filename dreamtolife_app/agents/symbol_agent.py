"""
SymbolAgent: detect symbols in the dream text using a knowledge base
of common dream symbols and their themes/meanings.
"""
import json
from pathlib import Path
import re

# Foundry IQ Integration: Import the knowledge retrieval layer for enriched lookups
from .foundry_iq import FoundryIQLayer


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

        # Foundry IQ Integration: Initialize the knowledge retrieval layer
        self.foundry_iq = FoundryIQLayer()
        
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
                    
                    # Foundry IQ Integration: Enrich symbol lookup with knowledge retrieval
                    # This retrieves grounded, cited information about the symbol
                    enriched_data = self.foundry_iq.retrieve(symbol, self.db)
                    
                    # Use themes from enriched retrieval if available, otherwise use index
                    if enriched_data.get("found") and enriched_data.get("results"):
                        # Add themes from Foundry IQ enriched results
                        for result in enriched_data["results"]:
                            for th in result.get("themes", []):
                                themes.add(th)
                    else:
                        # Graceful fallback: use original index themes
                        for th in sym_themes:
                            themes.add(th)
                    
                    break

        return sorted(list(found)), sorted(list(themes))
