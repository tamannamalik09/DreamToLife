"""
FoundryIQ Knowledge Retrieval Layer: Searches symbol database with grounded,
cited results and source attribution for enriched symbol lookups.
"""


class FoundryIQLayer:
    """
    Foundry IQ-style knowledge retrieval that searches a symbol database
    and returns grounded, cited results with source attribution.
    """

    def retrieve(self, query: str, db: dict) -> dict:
        """
        Search the symbol database for knowledge related to the query.
        
        Args:
            query: The search term or symbol name
            db: The symbols database dictionary
            
        Returns:
            A dictionary with 'results' (list of matching symbols with citations),
            'query' (the original query), and 'sources' (list of cited sources).
            Returns gracefully with empty results if nothing is found.
        """
        query_lower = query.lower()
        results = []
        sources = set()

        # Search through the database for matches
        for symbol, info in db.items():
            keywords = info.get("keywords", [])
            meanings = info.get("meanings", [])
            themes = info.get("themes", [])

            # Check if query matches the symbol name or any keywords
            if (query_lower in symbol.lower() or 
                any(query_lower in k.lower() for k in keywords)):
                
                # Build a grounded result with source attribution
                result_entry = {
                    "symbol": symbol,
                    "meanings": meanings,
                    "themes": themes,
                    "keywords": keywords,
                    "source": f"symbols.json",  # Source attribution
                    "cited": True
                }
                results.append(result_entry)
                sources.add("symbols.json")

        # Graceful fallback: return empty results structure if nothing found
        return {
            "results": results,
            "query": query,
            "sources": list(sources),
            "found": len(results) > 0
        }
