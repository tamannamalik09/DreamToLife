"""
EmotionAgent: improved keyword-based emotion detector.

This agent matches stems and keywords to a curated emotion mapping and
returns percentage scores (0-100) for multiple emotions. If no emotion is
detected, it returns {'Neutral': 100} as a gentle baseline.
"""
from collections import Counter
import re


class EmotionAgent:
    """Detects a range of emotions and returns percentage scores (ints).

    Emotions detected: Anxiety, Fear, Motivation, Curiosity, Excitement,
    Happiness, Stress, Loneliness, Confidence, Neutral
    """

    EMOTION_KEYWORDS = {
        "Anxiety": ["fall", "falling", "trapped", "lost", "late", "chase", "drown", "drowning", "panic", "anxious", "uneasy", "nervous"],
        "Fear": ["dark", "darkness", "monster", "snake", "danger", "death", "afraid", "scared", "terrified"],
        "Motivation": ["fly", "flying", "win", "winning", "success", "climb", "mountain", "achieve", "goal", "victory"],
        "Curiosity": ["explor", "exploring", "mystery", "unknown", "discover", "forest", "investigat", "wonder"],
        "Excitement": ["adventure", "celebration", "party", "excited", "thrill", "eager"],
        "Happiness": ["happy", "joy", "delight", "smile", "pleased", "content", "peace"],
        "Stress": ["stress", "stressed", "overwhelm", "pressure", "urgent"],
        "Loneliness": ["lonely", "alone", "isolat", "abandon", "left"],
        "Confidence": ["confident", "secure", "bold", "brave", "courage", "assured"]
    }

    WORD_RE = re.compile(r"\w+")

    def analyze(self, text: str) -> dict:
        """Return a dict of emotion -> percentage (0-100 ints).

        Multiple emotions can be present. Percentages sum to 100.
        """
        t = (text or "").lower()
        words = self.WORD_RE.findall(t)
        counts = Counter(words)

        # accumulate raw counts per emotion
        raw = {emo: 0 for emo in self.EMOTION_KEYWORDS}
        for emo, keys in self.EMOTION_KEYWORDS.items():
            for key in keys:
                for w, c in counts.items():
                    if key in w:
                        raw[emo] += c

        total = sum(raw.values())
        if total <= 0:
            return {"Neutral": 100}

        # compute float percentages
        floats = {emo: (cnt / total) * 100.0 for emo, cnt in raw.items() if cnt > 0}

        # round to ints but preserve sum=100 by distributing remainder
        ints = {emo: int(round(val)) for emo, val in floats.items()}
        s = sum(ints.values())
        # adjust small rounding diffs
        if s != 100:
            # compute remainders and sort by fractional part descending
            remainders = sorted(((emo, floats[emo] - ints.get(emo, 0)) for emo in floats), key=lambda x: x[1], reverse=True)
            diff = 100 - s
            idx = 0
            while diff != 0 and remainders:
                emo, _ = remainders[idx % len(remainders)]
                ints[emo] = ints.get(emo, 0) + (1 if diff > 0 else -1)
                diff = 100 - sum(ints.values())
                idx += 1

        # remove zero entries and return
        result = {emo: v for emo, v in ints.items() if v > 0}
        return result
