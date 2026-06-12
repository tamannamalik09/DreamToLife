"""
NarrativeAgent: converts dream analysis into human-readable interpretation.

Takes symbols, themes, emotions, and dream text to generate a 3-5 sentence
narrative summary that weaves these elements into a cohesive reflection.
"""


class NarrativeAgent:
    """Generates supportive, insightful dream narratives from analysis."""

    # Brief symbolic meanings for narrative context
    SYMBOL_MEANINGS = {
        "water": "emotional depths and the unconscious",
        "teeth": "power, control, or anxiety about appearance",
        "falling": "loss of control or instability",
        "flying": "freedom, escape, or liberation",
        "snake": "transformation, change, or a challenge",
        "house": "your sense of self and identity",
        "car": "your life direction and control",
        "baby": "new beginnings and potential",
        "school": "learning and evaluation",
        "naked": "vulnerability or authenticity",
        "chase": "avoidance or pressure",
        "fire": "passion, transformation, or anger",
        "bridge": "transition or connection",
        "knife": "conflict or a difficult decision",
        "blood": "life force or a wound",
        "mirror": "self-image and reflection",
        "money": "value and security",
        "death": "endings and new beginnings",
        "darkness": "the unknown or anxiety",
        "light": "clarity and insight",
        "forest": "exploration and mystery",
        "mountain": "a challenge or goal",
        "ocean": "vast emotions or the unconscious",
        "door": "opportunity or access",
        "key": "solution or understanding",
        "celebration": "joy and connection",
        "storm": "emotional turmoil",
        "bird": "freedom and perspective",
    }

    def generate(self, dream_text: str, symbols: list, themes: list, emotions: dict) -> str:
        """Generate a 3-5 sentence narrative from dream analysis.

        Args:
            dream_text: Original dream description
            symbols: List of detected symbols
            themes: List of detected themes
            emotions: Dict of emotions with percentage scores

        Returns:
            A narrative summary (3-5 sentences)
        """
        sentences = []

        # Sentence 1: Set the scene + primary symbol
        if symbols:
            primary_symbol = symbols[0]
            meaning = self._get_meaning(primary_symbol)
            scene = self._extract_scene(dream_text)
            sentences.append(f"Your dream unfolds in {scene}, where {primary_symbol} appears—representing {meaning}.")
        else:
            scene = self._extract_scene(dream_text)
            sentences.append(f"Your dream takes place in {scene}, exploring themes of transformation and self-awareness.")

        # Sentence 2: Weave in additional symbols
        if len(symbols) > 1:
            other = symbols[1:3]
            meanings = [f"{s} ({self._get_meaning(s)})" for s in other]
            sentences.append(f"Other elements present—{', '.join(meanings)}—add layers to this inner landscape.")
        elif themes:
            sentences.append(f"The dream emphasizes {', '.join(themes[:2])}—patterns worth exploring in your waking life.")

        # Sentence 3: Connect to emotions
        if emotions:
            top_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:2]
            emo_str = " and ".join([f"{e} ({p}%)" for e, p in top_emotions])
            primary_emotion = top_emotions[0][0]
            sentences.append(f"The dominant feeling is {emo_str}, suggesting {self._emotion_context(primary_emotion)} may be active.")

        # Sentence 4: Synthesis and invitation
        if symbols or themes:
            combined = (symbols + themes)[:3]
            sentences.append(f"Taken together, {', '.join(combined)} invite you to reflect on where you seek growth or face resistance.")

        # Sentence 5: Empowering closure (optional if we have enough)
        if len(emotions) > 0:
            sentences.append("This dream is an invitation to understand yourself more deeply—not to predict, but to illuminate.")

        return " ".join(sentences[:5])  # Ensure 3-5 sentences max

    def _get_meaning(self, symbol: str) -> str:
        """Retrieve brief symbolic meaning or return generic."""
        return self.SYMBOL_MEANINGS.get(symbol.lower(), "an inner truth or challenge")

    def _extract_scene(self, text: str) -> str:
        """Try to extract a scene descriptor from dream text."""
        # Simple heuristic: look for location keywords
        locations = ["forest", "house", "ocean", "mountain", "city", "room", "building", "school", "office"]
        t = text.lower()
        for loc in locations:
            if loc in t:
                return loc
        # Fallback: check for generic setting
        if "dark" in t or "darkness" in t:
            return "darkness"
        if "light" in t or "bright" in t:
            return "light"
        return "an inner landscape"

    def _emotion_context(self, emotion: str) -> str:
        """Map emotion to a context phrase."""
        contexts = {
            "Anxiety": "uncertainty or worry",
            "Fear": "something challenging or threatening",
            "Motivation": "ambition and drive",
            "Curiosity": "a desire to understand",
            "Excitement": "enthusiasm or anticipation",
            "Happiness": "joy and contentment",
            "Stress": "pressure or overwhelm",
            "Loneliness": "a need for connection",
            "Confidence": "strength and self-assurance",
            "Neutral": "observation and reflection",
        }
        return contexts.get(emotion, "reflection and insight")
