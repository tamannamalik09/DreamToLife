"""
CoordinatorAgent orchestrates the EmotionAgent, SymbolAgent, ActionAgent,
and GrowthAgent to analyze a dream and produce a combined report.
"""
from .agents.emotion_agent import EmotionAgent
from .agents.symbol_agent import SymbolAgent
from .agents.action_agent import ActionAgent
from .agents.growth_agent import GrowthAgent
from .agents.narrative_agent import NarrativeAgent
from .journal import DreamJournal
from .image_prompt import ImagePromptGenerator
from datetime import datetime
import json


class CoordinatorAgent:
    """Top-level orchestrator that sends dream text to each agent and
    aggregates their outputs into a single DreamToLife report dict.
    """

    def __init__(self):
        self.emotion_agent = EmotionAgent()
        self.symbol_agent = SymbolAgent()
        self.action_agent = ActionAgent()
        self.growth_agent = GrowthAgent()
        self.narrative_agent = NarrativeAgent()
        self.image_prompt = ImagePromptGenerator()

    def analyze_dream(self, dream_text: str) -> dict:
        """Main entry: send dream text to all agents and combine results.

        Returns a dictionary containing the full report and metadata.
        """
        # Emotion analysis
        emotions = self.emotion_agent.analyze(dream_text)

        # Symbol & theme extraction
        symbols, themes = self.symbol_agent.extract(dream_text)

        # Actions and reflection
        daily_action, weekly_challenge, reflection_questions = self.action_agent.suggest(
            themes, emotions
        )

        # Growth insights (based on existing journal)
        growth_insight = self.growth_agent.summarize_from_text(dream_text, symbols, emotions)

        # Narrative interpretation
        narrative = self.narrative_agent.generate(dream_text, symbols, themes, emotions)

        # Scorecard heuristics
        scorecard = self._compute_scorecard(emotions, themes)

        # Image prompt (mock)
        image_prompt = self.image_prompt.generate(dream_text)

        # Build summary
        summary = self._build_summary(dream_text)

        # Combine into report
        report = {
            "date": datetime.utcnow().isoformat(),
            "dream_text": dream_text,
            "summary": summary,
            "emotions": emotions,
            "symbols": symbols,
            "themes": themes,
            "daily_action": daily_action,
            "weekly_challenge": weekly_challenge,
            "reflection_questions": reflection_questions,
            "growth_insight": growth_insight,
            "narrative": narrative,
            "scorecard": scorecard,
            "image_prompt": image_prompt,
        }

        # Also include a printable report text for storage convenience
        report_text = self._format_report_text(report)
        report["report_text"] = report_text

        return report

    def _build_summary(self, dream_text: str) -> str:
        # Simple summary: first 1-2 sentences or truncated text
        text = dream_text.strip()
        if "." in text:
            return text.split(".")[0].strip() + "."
        return text if len(text) < 300 else text[:300] + "..."

    def _compute_scorecard(self, emotions: dict, themes: list) -> dict:
        # Emotional intensity: handle either 0-1 floats or 0-100 percentages
        max_emotion = max(emotions.values()) if emotions else 0
        if max_emotion > 1:
            emotional_intensity = min(100, int(max_emotion))
        else:
            emotional_intensity = min(100, int(max_emotion * 100))
        # Reflection depth: number of reflection questions detected
        reflection_depth = min(100, 10 * len(themes))
        # Growth opportunity: function of novelty and intensity
        growth_opportunity = min(100, int((emotional_intensity * 0.5) + (reflection_depth * 0.5)))
        return {
            "Emotional Intensity": emotional_intensity,
            "Reflection Depth": reflection_depth,
            "Growth Opportunity": growth_opportunity,
        }

    def _format_report_text(self, report: dict) -> str:
        # Compact text version stored in journal (human readable)
        lines = []
        lines.append("🌙 DREAMTOLIFE REPORT")
        lines.append("📝 Summary: " + report.get("summary", ""))
        lines.append("🎭 Emotions:")
        for k, v in report.get("emotions", {}).items():
            lines.append(f" - {k}: {v}%")
        lines.append("🔍 Symbols: " + ", ".join(report.get("symbols", [])))
        lines.append("💡 Themes: " + ", ".join(report.get("themes", [])))
        lines.append("📖 Narrative: " + report.get("narrative", ""))
        lines.append("✅ Daily Action: " + report.get("daily_action", ""))
        lines.append("🎯 Weekly Challenge: " + report.get("weekly_challenge", ""))
        lines.append("🌱 Growth Insight: " + report.get("growth_insight", ""))
        lines.append("📊 Scorecard: " + ", ".join(f"{k}={v}" for k, v in report.get("scorecard", {}).items()))
        return "\n".join(lines)
