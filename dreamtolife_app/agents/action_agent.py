"""
ActionAgent: convert detected themes and emotions into actionable
personal-growth steps: a daily action, a weekly challenge, and reflection
questions.
"""
from random import choice


class ActionAgent:
    """Turn themes and emotions into concrete suggestions."""

    def suggest(self, themes: list, emotions: dict):
        # Simple heuristics to generate actions
        primary_emotion = max(emotions, key=emotions.get) if emotions else "neutral"

        # Daily action: small, concrete habit
        if themes:
            daily = f"Spend 10 minutes journaling about '{themes[0]}' and how it shows up in your life."
        else:
            daily = "Spend 10 minutes grounding (deep breathing, walk)."

        # Weekly challenge: slightly larger practice
        if themes:
            weekly = f"This week, notice one situation that relates to '{themes[0]}' and act with curiosity rather than judgment."
        else:
            weekly = "Try a 30-minute reflection session about recent emotions and patterns."

        # Reflection questions
        questions = []
        questions.append(f"When have you felt '{primary_emotion}' recently in waking life?")
        if themes:
            questions.append(f"Where else in your life does the theme '{themes[0]}' show up?")
            questions.append(f"What small step could honor or address '{themes[0]}' this week?")

        return daily, weekly, questions
